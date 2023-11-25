import math
from typing import Dict, Union

import forallpeople as si

si.environment('structural', top_level=False)

cm = si.m / 100


class CountryFactors:
    COUNTRY_FACTORS: Dict[str, Dict[str, int]] = {
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
    BUCKLING_CURVES: Dict[str, int] = {
        'a0': 0.13,
        'a': 0.21,
        'b': 0.34,
        'c': 0.49,
        'd': 0.76,
    }

    BUCKLING_types: Dict[str, str] = {'CF': "c", 'HF': "a"}

    def chosen_type_profile(self, type_of_profile: str) -> str:
        for key, value in self.BUCKLING_types.items():
            if type_of_profile in key:
                return self.BUCKLING_types[type_of_profile]
        print("Check profile")

    def buckling_curve(self, buckling_curve: str) -> float:
        for key, value in self.BUCKLING_CURVES.items():
            if buckling_curve in key:
                return self.BUCKLING_CURVES[buckling_curve]
        print("Check chosen curve")


class ProfileRhs:
    def __init__(
        self,
        type_profile: str,
        sectional_area: float,
        height_profile: int,
        width_profile: int,
        thickness_flange: int,
        second_moment_area_y: float,
        second_moment_area_z: float,
        yield_strength: int,
        length: Union[int, float],
        plastic_section_y: float,
        plastic_section_z: float,
    ) -> None:
        self.type_profile = type_profile
        self.A = sectional_area * si.mm**2
        self.H = height_profile * si.mm
        self.B = width_profile * si.mm
        self.T = thickness_flange * si.mm
        self.Iy = second_moment_area_y * si.mm**4
        self.Iz = second_moment_area_z * si.mm**4
        self.Fy = yield_strength
        self.Wply = plastic_section_y * si.mm**3
        self.Wplz = plastic_section_z * si.mm**3
        self.L = length * si.m
        self.G = SteelGrade().WEIGHT

    def weight_per_m(self) -> float:
        return self.A * self.G

    def radius_of_gyration_iy(self):
        iy = self.Iy / self.A
        return math.sqrt(iy) * si.mm

    def radius_of_gyration_iz(self):
        iz = self.Iz / self.A
        return math.sqrt(iz) * si.mm

    def shear_area_z(self):
        Az = (self.A * self.H) / (self.B + self.H)
        return Az

    def shear_area_y(self):
        Ay = (self.A * self.B) / (self.B + self.H)
        return Ay


class ReductionBucklingFactorsCFRHS(ProfileRhs):
    def __init__(
        self,
        type_profile: str,
        sectional_area: float,
        height_profile: int,
        width_profile: int,
        thickness_flange: int,
        second_moment_area_y: float,
        second_moment_area_z: float,
        yield_strength: int,
        length: Union[int, float],
        plastic_section_y: float,
        plastic_section_z: float,
        buckling_factor: float,
    ):
        super().__init__(
            type_profile,
            sectional_area,
            height_profile,
            width_profile,
            thickness_flange,
            second_moment_area_y,
            second_moment_area_z,
            yield_strength,
            length,
            plastic_section_y,
            plastic_section_z,
        )
        self.buckling_factor = buckling_factor
        self.curve_for_chosen_profile = BucklingCurves().chosen_type_profile(
            type_profile
        )
        self.buckling_curve = BucklingCurves().buckling_curve(
            self.curve_for_chosen_profile
        )
        self.E = SteelGrade().MODULUS_OF_ELASTICITY
        self.iy = self.radius_of_gyration_iy()
        self.iz = self.radius_of_gyration_iz()

    def epsilon(self) -> float:
        yield_strength = self.Fy / si.MPa
        return math.sqrt(235 / yield_strength)

    def lambda_slenderness_1(self) -> float:
        return math.pi * (math.sqrt((self.E / self.Fy)))

    def buckling_length(self) -> float:
        return self.L * self.buckling_factor

    def lambda_relative_slenderness_y(self) -> float:
        return (self.buckling_length() / self.iy) * (1 / self.lambda_slenderness_1())

    def theta_reduction_factor_y(
        self,
    ) -> float:
        return 0.5 * (
            1
            + self.buckling_curve * (self.lambda_relative_slenderness_y() - 0.2)
            + (self.lambda_relative_slenderness_y() ** 2)
        )

    def chi_reduction_factor_y(self) -> float:
        chi = 1 / (
            self.theta_reduction_factor_y()
            + math.sqrt(
                (self.theta_reduction_factor_y() ** 2)
                - (self.lambda_relative_slenderness_y() ** 2)
            )
        )
        return min(chi, 1.0)

    def lambda_relative_slenderness_z(self) -> float:
        return (self.buckling_length() / self.iz) * (1 / self.lambda_slenderness_1())

    def theta_reduction_factor_z(
        self,
    ) -> float:
        return 0.5 * (
            1
            + self.buckling_curve * (self.lambda_relative_slenderness_z() - 0.2)
            + (self.lambda_relative_slenderness_z() ** 2)
        )

    def chi_reduction_factor_z(self) -> float:
        chi = 1 / (
            self.theta_reduction_factor_z()
            + math.sqrt(
                (self.theta_reduction_factor_z() ** 2)
                - (self.lambda_relative_slenderness_z() ** 2)
            )
        )
        return min(chi, 1.0)


class CalculationCFRHS(ReductionBucklingFactorsCFRHS):
    def __init__(
        self,
        type_profile: str,
        sectional_area: float,
        height_profile: int,
        width_profile: int,
        thickness_flange: int,
        second_moment_area_y: float,
        second_moment_area_z: float,
        yield_strength: int,
        length: Union[int, float],
        plastic_section_y: float,
        plastic_section_z: float,
        buckling_factor: Union[int, float],
        sectional_axial_force: Union[int, float],
        sectional_bending_moment_y: Union[int, float],
        sectional_bending_moment_z: Union[int, float],
        sectional_shear_y: Union[int, float],
        sectional_shear_z: Union[int, float],
        eccentricity: Union[int, float],
        gammas: Dict[str, float],
        limit_deformation: Union[int, float],
    ):
        super().__init__(
            type_profile,
            sectional_area,
            height_profile,
            width_profile,
            thickness_flange,
            second_moment_area_y,
            second_moment_area_z,
            yield_strength,
            length,
            plastic_section_y,
            plastic_section_z,
            buckling_factor,
        )

        self.Az = self.shear_area_z()
        self.Ay = self.shear_area_y()
        self.Ned = sectional_axial_force * si.kN
        self.Med_y = sectional_bending_moment_y * si.kN * si.m
        self.Med_z = sectional_bending_moment_z * si.kN * si.m
        self.Ved_z = sectional_shear_z * si.kN
        self.Ved_y = sectional_shear_y * si.kN
        self.ecc = eccentricity * si.mm
        self.ym0 = gammas['ym0']
        self.ym1 = gammas['ym1']
        self.ym2 = gammas['ym2']
        self.E = SteelGrade().MODULUS_OF_ELASTICITY
        self.limit_deformation = limit_deformation
        self.Fy = yield_strength * self.reduction_due_shear()

    def tension_profile(self) -> float:
        return (self.A * self.Fy) / self.ym0

    def bending_capacity_profile_y(self) -> float:
        return self.Wply * self.Fy / self.ym0

    def bending_capacity_profile_z(self) -> float:
        return self.Wplz * self.Fy / self.ym0

    def reduction_bending_capacity_factors(self) -> tuple[float, float]:
        n = self.Ned / self.tension_profile()

        aw = min((self.A - 2 * self.B * self.T) / self.A, 0.5)
        af = min((self.A - 2 * self.H * self.T) / self.A, 0.5)

        qn_y = max((1 - n / 100) / (1 - 0.5 * aw), 0.01)
        qn_z = max((1 - n / 100) / (1 - 0.5 * af), 0.01)

        return qn_y, qn_z

    def reduced_bending_capacity_y(self):
        qn_y, qn_z = self.reduction_bending_capacity_factors()
        return min(
            self.bending_capacity_profile_y() * qn_y, self.bending_capacity_profile_y()
        )

    def reduced_bending_capacity_z(self):
        qn_y, qn_z = self.reduction_bending_capacity_factors()
        return min(
            self.bending_capacity_profile_z() * qn_z, self.bending_capacity_profile_z()
        )

    def reduction_biaxial_bending_capacity(self):
        n = self.Ned / self.tension_profile()
        alpha = 1.66 / (1 - (1.13 * (n**2)))
        alpha = min(alpha, 6)
        beta = alpha
        ur = (self.Med_y / self.reduced_bending_capacity_y()) ** alpha + (
            self.Med_z / self.reduced_bending_capacity_y()
        ) ** beta
        return ur

    def compression_capacity_y(self) -> float:
        return (self.A * self.Fy * self.chi_reduction_factor_y()) / self.ym1

    def compression_capacity_z(self) -> float:
        return (self.A * self.Fy * self.chi_reduction_factor_z()) / self.ym1

    def load_from_self_weight(self) -> float:
        return self.weight_per_m() * 0.01 * si.kN / si.kg

    def bending_from_self_weight(self) -> float:
        return (self.load_from_self_weight() * self.L**2) / 8

    def bending_from_eccentricity(self) -> float:
        return self.Ned * self.ecc

    def total_bending(self) -> float:
        return (
            self.bending_from_self_weight()
            + self.bending_from_eccentricity()
            + self.Med_y
        )

    def bending_capacity_y(self) -> float:
        return self.Wply * self.Fy / self.ym1

    def bending_capacity_z(self) -> float:
        return self.Wplz * self.Fy / self.ym1

    def shear_capacity_z(self) -> float:
        return self.Az * self.Fy / (math.sqrt(3) * self.ym0)

    def shear_capacity_y(self) -> float:
        return self.Ay * self.Fy / (math.sqrt(3) * self.ym0)

    def reduction_due_shear(self) -> float:
        if (
            self.Ved_y > self.shear_capacity_y() / 2
            or self.Ved_z > self.shear_capacity_z() / 2
        ):
            q_y = (((2 * self.Ved_y) / self.shear_capacity_y()) - 1) ** 2
            q_z = (((2 * self.Ved_z) / self.shear_capacity_z()) - 1) ** 2
            return min(q_y, q_z)
        return 1.0

    def deflection_self_weight(self) -> float:
        return (5 * self.load_from_self_weight() * self.L**4) / (
            384 * self.E * self.Iy
        )

    # def deflection_bending(self) -> float:
    #     bending_moment = self.Med + self.bending_from_eccentricity()
    #     return (bending_moment * self.L ** 2) / (8 * self.E * self.Iy)
    #
    # def total_deflection(self) -> float:
    #     return self.deflection_bending() + self.deflection_self_weight()
    #
    # def check_deformation(self) -> float:
    #     limit = self.L / self.limit_deformation
    #     return self.total_deflection() / limit
    #
    # def check_utilization_with_compression(self) -> float:
    #     axial_ur = self.Ned / self.compression_capacity()
    #     bending_ur = self.total_bending() / self.bending_capacity()
    #     return axial_ur + bending_ur + 0.01
    #
    # def check_utilization_with_tension(self) -> float:
    #     axial_ur = self.Ned / self.tension_capacity()
    #     bending_ur = self.total_bending() / self.bending_capacity()
    #     return axial_ur + bending_ur + 0.01


if __name__ == "__main__":
    gammas = CountryFactors()
    gammas_country = gammas.finding_gammas("Sweden")
    steel = SteelGrade()
    steel_grade = steel.finding_steel("S275")

    # 80x60x5
    obiekt = CalculationCFRHS(
        type_profile='CF',
        sectional_area=1236,
        height_profile=80,
        width_profile=60,
        thickness_flange=5,
        second_moment_area_y=1032754,
        second_moment_area_z=656611,
        yield_strength=steel_grade,
        length=5,
        plastic_section_y=32235,
        plastic_section_z=26379,
        buckling_factor=1,
        sectional_axial_force=30,
        sectional_bending_moment_y=10,
        sectional_bending_moment_z=10,
        sectional_shear_y=10,
        sectional_shear_z=10,
        eccentricity=0,
        gammas=gammas_country,
        limit_deformation=200,
    )

    print(
        obiekt.radius_of_gyration_iy(),
        obiekt.radius_of_gyration_iz(),
        obiekt.reduction_bending_capacity_factors(),
        obiekt.reduced_bending_capacity_y(),
        obiekt.reduced_bending_capacity_z(),
        obiekt.reduction_biaxial_bending_capacity(),
        obiekt.compression_capacity_y(),
        obiekt.compression_capacity_z(),
    )
