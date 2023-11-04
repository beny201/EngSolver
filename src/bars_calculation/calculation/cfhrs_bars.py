import math
from typing import Dict, Union

import forallpeople as si

si.environment('structural', top_level=False)

cm = si.m / 100


class CountryFactors:
    COUNTRY_FACTORS = {
        'Norway': {'ym0': 1.05, 'ym1': 1.05, 'ym2': 1.25},
        'Sweden': {'ym0': 1.00, 'ym1': 1.00, 'ym2': 1.25},
        'Denmark': {'ym0': 1.10, 'ym1': 1.20, 'ym2': 1.35},
        'Germany': {'ym0': 1.00, 'ym1': 1.10, 'ym2': 1.25},
    }

    def finding_gammas(self, country: str) -> Dict[str, float]:
        for key, values in self.COUNTRY_FACTORS.items():
            if country in key:
                return self.COUNTRY_FACTORS[key]


class SteelGrade:
    MODULUS_OF_ELASTICITY = 210_000 * si.MPa
    WEIGHT = 7900 * si.kg / si.m**3

    STEEL_GRADE = {
        'S235': 235 * si.MPa,
        'S275': 275 * si.MPa,
        'S355': 355 * si.MPa,
    }

    def finding_steel(self, steel: str) -> int:
        for key, values in self.STEEL_GRADE.items():
            if steel in key:
                return self.STEEL_GRADE[steel]


class BucklingCurves:
    BUCKLING_CURVES = {
        'a0': 0.13,
        'a': 0.21,
        'b': 0.34,
        'c': 0.49,
        'd': 0.76,
    }

    def buckling_curve(self, buckling_curve: str) -> float:
        for key, value in self.BUCKLING_CURVES.items():
            if buckling_curve in key:
                return self.BUCKLING_CURVES[buckling_curve]
        else:
            print("Check chosen curve")


class ProfileCFRHS:
    def __init__(
        self,
        sectional_area: float,
        second_moment_area: float,
        radius_of_gyration: float,
        yield_strength: int,
        length: Union[int, float],
        plastic_section: float,
    ):
        self.sectional_area = sectional_area * cm**2
        self.second_moment_area = second_moment_area * cm**4
        self.radius_of_gyration = radius_of_gyration * si.mm
        self.yield_strength = yield_strength
        self.plastic_section = plastic_section * cm**3
        self.length = length * si.m
        self.WEIGHT = SteelGrade().WEIGHT

    def weight_per_m(self) -> float:
        return self.sectional_area * self.WEIGHT


class ReductionFactorsCFRHS(ProfileCFRHS):
    def __init__(
        self,
        sectional_area: float,
        second_moment_area: float,
        radius_of_gyration: float,
        yield_strength: int,
        length: Union[int, float],
        plastic_section: float,
    ):
        super().__init__(
            sectional_area,
            second_moment_area,
            radius_of_gyration,
            yield_strength,
            length,
            plastic_section,
        )
        self.buckling_factor = 1
        self.buckling_curve = BucklingCurves().buckling_curve("c")
        self.MODULUS_OF_ELASTICITY = SteelGrade().MODULUS_OF_ELASTICITY

    def epsilon(self) -> float:
        yield_strength = self.yield_strength / si.MPa
        return math.sqrt(235 / yield_strength)

    def lambda_slenderness_1(self) -> float:
        return math.pi * (math.sqrt((self.MODULUS_OF_ELASTICITY / self.yield_strength)))

    def buckling_length(self) -> float:
        return self.length * self.buckling_factor

    def lambda_relative_slenderness(
        self,
    ) -> float:
        return (self.buckling_length() / self.radius_of_gyration) * (
            1 / self.lambda_slenderness_1()
        )

    def theta_reduction_factor(
        self,
    ) -> float:
        return 0.5 * (
            1
            + self.buckling_curve * (self.lambda_relative_slenderness() - 0.2)
            + self.lambda_relative_slenderness() ** 2
        )

    def chi_reduction_factor(self) -> float:
        chi = 1 / (
            self.theta_reduction_factor()
            + math.sqrt(
                (self.theta_reduction_factor() ** 2)
                - (self.lambda_relative_slenderness() ** 2)
            )
        )
        if chi <= 1:
            return chi
        else:
            return 1.0


class CalculationCFRHS(ReductionFactorsCFRHS):
    def __init__(
        self,
        sectional_area: float,
        second_moment_area: float,
        radius_of_gyration: float,
        yield_strength: int,
        length: Union[int, float],
        plastic_section: float,
        sectional_axial_force: Union[int, float],
        sectional_bending_moment: Union[int, float],
        eccentricity: Union[int, float],
        gammas: Dict[str, float],
        limit_deformation: Union[int, float],
    ):
        super().__init__(
            sectional_area,
            second_moment_area,
            radius_of_gyration,
            yield_strength,
            length,
            plastic_section,
        )

        self.sectional_axial_force = sectional_axial_force * si.kN
        self.sectional_bending_moment = sectional_bending_moment * si.kN * si.m
        self.eccentricity = eccentricity * si.mm
        self.gamma_0 = gammas['ym0']
        self.gamma_1 = gammas['ym1']
        self.gamma_2 = gammas['ym2']
        self.MODULUS_OF_ELASTICITY = SteelGrade().MODULUS_OF_ELASTICITY
        self.limit_deformation = limit_deformation

    def tension_capacity(self) -> float:
        return (self.sectional_area * self.yield_strength) / self.gamma_1

    def compression_capacity(self) -> float:
        return (
            self.sectional_area * self.yield_strength * self.chi_reduction_factor()
        ) / self.gamma_1

    def load_from_self_weight(self) -> float:
        return self.weight_per_m() * 0.01 * si.kN / si.kg

    def bending_from_self_weight(self) -> float:
        return (self.load_from_self_weight() * self.length**2) / 8

    def bending_from_eccentricity(self) -> float:
        return self.sectional_axial_force * self.eccentricity

    def total_bending(self) -> float:
        return (
            self.bending_from_self_weight()
            + self.bending_from_eccentricity()
            + self.sectional_bending_moment
        )

    def bending_capacity(self) -> float:
        return self.plastic_section * self.yield_strength / self.gamma_1

    def deflection_self_weight(self) -> float:
        return (5 * self.load_from_self_weight() * self.length**4) / (
            384 * self.MODULUS_OF_ELASTICITY * self.second_moment_area
        )

    def deflection_bending(self) -> float:
        bending_moment = (
            self.sectional_bending_moment + self.bending_from_eccentricity()
        )
        return (bending_moment * self.length**2) / (
            8 * self.MODULUS_OF_ELASTICITY * self.second_moment_area
        )

    def total_deflection(self) -> float:
        return self.deflection_bending() + self.deflection_self_weight()

    def check_deformation(self) -> float:
        limit = self.length / self.limit_deformation
        return self.total_deflection() / limit

    def check_utilization_with_compression(self) -> float:
        axial_ur = self.sectional_axial_force / self.compression_capacity()
        bending_ur = self.total_bending() / self.bending_capacity()
        return axial_ur + bending_ur + 0.01

    def check_utilization_with_tension(self) -> float:
        axial_ur = self.sectional_axial_force / self.tension_capacity()
        bending_ur = self.total_bending() / self.bending_capacity()
        return axial_ur + bending_ur + 0.01
