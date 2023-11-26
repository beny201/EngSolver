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
        eccentricity_y: Union[int, float],
        eccentricity_z: Union[int, float],
        gammas: Dict[str, float],
        limit_deformation: Union[int, float],
        main_axis: str,
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
        self.ecc_y = eccentricity_y * si.mm
        self.ecc_z = eccentricity_z * si.mm
        self.ym0 = gammas['ym0']
        self.ym1 = gammas['ym1']
        self.ym2 = gammas['ym2']
        self.E = SteelGrade().MODULUS_OF_ELASTICITY
        self.limit_deformation = limit_deformation
        self.Fy = yield_strength * self.reduction_due_shear()
        self.main_axis = main_axis
        self.Med_y = self.total_bending_my()
        self.Med_z = self.total_bending_mz()

    def shear_capacity_z(self) -> float:
        return self.Az * self.Fy / (math.sqrt(3) * self.ym0)

    def shear_capacity_y(self) -> float:
        return self.Ay * self.Fy / (math.sqrt(3) * self.ym0)

    def check_shear_capacity_z(self) -> float:
        return self.Fz / self.shear_capacity_z()

    def check_shear_capacity_y(self) -> float:
        return self.Fy / self.shear_capacity_y()

    def check_total_shear(self) -> float:
        ur1 = self.check_shear_capacity_z()
        ur2 = self.check_shear_capacity_y()
        return max(ur1, ur2)

    def reduction_due_shear(self) -> float:
        if (
            self.Ved_y > self.shear_capacity_y() / 2
            or self.Ved_z > self.shear_capacity_z() / 2
        ):
            q_y = (((2 * self.Ved_y) / self.shear_capacity_y()) - 1) ** 2
            q_z = (((2 * self.Ved_z) / self.shear_capacity_z()) - 1) ** 2
            return min(q_y, q_z)
        return 1.0

    def tension_profile(self) -> float:
        return (self.A * self.Fy) / self.ym0

    def check_tension_profile(self) -> float:
        return self.Ned / self.tension_profile()

    def bending_capacity_profile_y(self) -> float:
        return self.Wply * self.Fy / self.ym0

    def bending_capacity_profile_z(self) -> float:
        return self.Wplz * self.Fy / self.ym0

    def reduction_bending_capacity_factors(self) -> tuple[float, float]:
        n = self.Ned / self.tension_profile()

        aw = min((self.A - 2 * self.B * self.T) / self.A, 0.5)
        af = min((self.A - 2 * self.H * self.T) / self.A, 0.5)
        qn_y = max((1 - n) / (1 - 0.5 * aw), 0.01)
        qn_z = max((1 - n) / (1 - 0.5 * af), 0.01)
        return qn_y, qn_z

    def reduced_bending_capacity_y(self) -> float:
        qn_y, qn_z = self.reduction_bending_capacity_factors()
        return min(
            self.bending_capacity_profile_y() * qn_y, self.bending_capacity_profile_y()
        )

    def reduced_bending_capacity_z(self) -> float:
        qn_y, qn_z = self.reduction_bending_capacity_factors()
        return min(
            self.bending_capacity_profile_z() * qn_z, self.bending_capacity_profile_z()
        )

    def reduction_biaxial_bending_capacity(self) -> float:
        n = self.Ned / self.tension_profile()
        alpha = max(1.66 / (1 - (1.13 * (n**2))), 1)
        alpha = min(alpha, 6)

        beta = alpha

        ur = (self.Med_y / self.reduced_bending_capacity_y()) ** alpha + (
            self.Med_z / self.reduced_bending_capacity_y()
        ) ** beta
        return ur

    def check_interaction_axial_force_and_bending(self) -> float:
        ur = max(
            self.Med_y / self.reduced_bending_capacity_y(),
            self.Med_z / self.reduced_bending_capacity_z(),
            self.reduction_biaxial_bending_capacity(),
        )
        return ur

    def compression_capacity_y(self) -> float:
        return (self.A * self.Fy * self.chi_reduction_factor_y()) / self.ym1

    def compression_capacity_z(self) -> float:
        return (self.A * self.Fy * self.chi_reduction_factor_z()) / self.ym1

    def check_buckling_y(self) -> float:
        return self.Ned / self.compression_capacity_y()

    def check_buckling_z(self) -> float:
        return self.Ned / self.compression_capacity_z()

    def check_total_buckling(self) -> float:
        ur1 = self.check_buckling_z()
        ur2 = self.check_buckling_y()
        return max(ur1, ur2)

    def load_from_self_weight(self) -> float:
        return self.weight_per_m() * 0.01 * si.kN / si.kg

    def bending_from_self_weight(self) -> float:
        return (self.load_from_self_weight() * self.L**2) / 8

    def bending_from_eccentricity_y(self) -> float:
        return self.Ned * self.ecc_y

    def bending_from_eccentricity_z(self) -> float:
        return self.Ned * self.ecc_z

    def total_bending_my(self) -> float:
        Med_y = self.bending_from_eccentricity_y() + self.Med_y
        if self.main_axis == "z":
            return Med_y + self.bending_from_self_weight()
        else:
            return Med_y

    def total_bending_mz(self) -> float:
        Med_z = self.bending_from_eccentricity_z() + self.Med_z
        if self.main_axis == "y":
            return Med_z + self.bending_from_self_weight()
        else:
            return Med_z

    def bending_capacity_y(self) -> float:
        return self.Wply * self.Fy / self.ym1

    def check_bending_y(self) -> float:
        return self.Med_y / self.bending_capacity_y()

    def bending_capacity_z(self) -> float:
        return self.Wplz * self.Fy / self.ym1

    def check_bending_z(self) -> float:
        return self.Med_z / self.bending_capacity_z()

    def check_total_bending(self):
        ur1 = self.check_bending_y()
        ur2 = self.check_bending_z()
        return max(ur1, ur2)

    # Buckling interaction for bending and axial compression Annex B method 2

    def Cmy(self):
        # assumption that there are hinge on both side of bar
        alfa_h = 0
        Cmy = max((0.95 + 0.05 * alfa_h), (0.9 + 0.1 * alfa_h))
        return max(Cmy, 0.4)

    def kyy(self) -> float:
        ur_y = self.check_buckling_y()
        fyy = min(self.lambda_relative_slenderness_y() - 0.2, 0.8)
        kyy = self.Cmy() * (1 + fyy * ur_y)
        return kyy

    def kzz(self) -> float:
        ur_z = self.check_buckling_z()
        fzz = min(self.lambda_relative_slenderness_z() - 0.2, 0.8)
        kzz = self.Cmy() * (1 + fzz * ur_z)
        return kzz

    def kzy(self) -> float:
        return 0.6 * self.kyy()

    def kyz(self) -> float:
        return 0.6 * self.kzz()

    def check_interaction_buckling_and_bending(self) -> float:
        ur1 = (
            self.check_buckling_y()
            + self.kyy() * self.check_bending_y()
            + self.kyz() * self.check_bending_z()
        )

        ur2 = (
            self.check_buckling_z()
            + self.kzy() * self.check_bending_y()
            + self.kzz() * self.check_bending_z()
        )
        return max(ur1, ur2)

    def deflection_self_weight(self) -> float:
        return (5 * self.load_from_self_weight() * self.L**4) / (
            384 * self.E * self.Iy
        )

    def deflection_bending_y(self) -> float:
        bending_moment = self.Med_y
        return (bending_moment * self.L**2) / (8 * self.E * self.Iy)

    def deflection_bending_z(self) -> float:
        bending_moment = self.Med_z
        return (bending_moment * self.L**2) / (8 * self.E * self.Iz)

    def check_deformation_y(self) -> float:
        limit = self.L / self.limit_deformation
        if self.main_axis == "z":
            ur1 = (self.deflection_bending_y() + self.deflection_self_weight()) / limit
        else:
            ur1 = self.deflection_bending_y() / limit
        return ur1

    def check_deformation_z(self) -> float:
        limit = self.L / self.limit_deformation
        if self.main_axis != "z":
            ur1 = (self.deflection_bending_z() + self.deflection_self_weight()) / limit
        else:
            ur1 = self.deflection_bending_z() / limit
        return ur1

    def check_deformation(self) -> float:
        ur1 = self.check_deformation_y()
        ur2 = self.check_deformation_z()
        return max(ur1, ur2)

    def check_when_tensioned_and_bended(self):
        ur1 = self.check_total_shear()
        ur2 = self.check_tension_profile()
        ur3 = self.check_interaction_axial_force_and_bending()
        ur4 = self.check_deformation()
        return max(ur1, ur2, ur3, ur4)

    def check_when_compressed_and_bended(self):
        ur1 = self.check_total_buckling()
        ur2 = self.check_total_bending()
        ur3 = self.check_interaction_buckling_and_bending()
        ur4 = self.check_deformation()
        return max(ur1, ur2, ur3, ur4)


if __name__ == "__main__":
    gammas = CountryFactors()
    gammas_country = gammas.finding_gammas("Sweden")
    steel = SteelGrade()
    steel_grade = steel.finding_steel("S275")

    # 80x60x5
    obiekt = CalculationCFRHS(
        type_profile='CF',
        sectional_area=11.8 * (10**2),
        height_profile=80,
        width_profile=80,
        thickness_flange=4,
        second_moment_area_y=111 * (10**4),
        second_moment_area_z=111 * (10**4),
        yield_strength=steel_grade,
        length=5,
        plastic_section_y=33.08 * (10**3),
        plastic_section_z=33.08 * (10**3),
        buckling_factor=1,
        sectional_axial_force=50,
        sectional_bending_moment_y=6.25,
        sectional_bending_moment_z=0,
        sectional_shear_y=0,
        sectional_shear_z=0,
        eccentricity_y=0,
        eccentricity_z=0,
        gammas=gammas_country,
        limit_deformation=200,
        main_axis="z",
    )

    print(
        # obiekt.compression_capacity_y(),
        # obiekt.lambda_relative_slenderness_y(),
        # obiekt.check_total_buckling(),
        # obiekt.bending_capacity_y(),
        # obiekt.check_bending_y(),
        # obiekt.reduced_bending_capacity_y(),
        # obiekt.kyy(),
        # obiekt.kzy(),
        # obiekt.check_interaction_buckling_and_bending(),
        obiekt.check_interaction_axial_force_and_bending(),
        obiekt.check_tension_profile(),
        # obiekt.deflection_bending_y(),
    )
