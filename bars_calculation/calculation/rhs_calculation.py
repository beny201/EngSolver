import math
from typing import Dict, Union

import forallpeople as si

from .buckling_parameters import ReductionBucklingFactorsRHS
from .force_to_calculation import ForceToCalculation
from .profile_to_calculation import ProfileRhsToCalculation
from .structural_parameters import CountryFactors, SteelGrade

si.environment('structural', top_level=False)

cm = si.m / 100


class CalculationRHS:
    def __init__(
        self,
        sectional_forces: ForceToCalculation,
        gammas: Dict[str, float],
        limit_deformation: Union[int, float],
        main_axis: str,
        profile: ProfileRhsToCalculation,
        buckling_factor: ReductionBucklingFactorsRHS,
        section_class: int,
    ):
        self.force = sectional_forces
        self.profile = profile
        self.buckling_factor = buckling_factor
        self.ym0 = gammas['ym0']
        self.ym1 = gammas['ym1']
        self.ym2 = gammas['ym2']
        self.limit_deformation = limit_deformation
        self.Fy_shear = self.profile.Fy
        self.profile.Fy = self.profile.Fy * (1 - self.reduction_due_shear())
        self.main_axis = main_axis
        self.E = SteelGrade().MODULUS_OF_ELASTICITY
        self.section_class = section_class
        self.Wply = self.switching_to_Wely()
        self.Wplz = self.switching_to_Welz()

    def switching_to_Wely(self):
        if self.section_class > 2:
            return self.profile.Wely
        else:
            return self.profile.Wply

    def switching_to_Welz(self):
        if self.section_class > 2:
            return self.profile.Welz
        else:
            return self.profile.Wplz

    def shear_capacity_z(self) -> float:
        return self.profile.Az * self.Fy_shear / (math.sqrt(3) * self.ym0)

    def shear_capacity_y(self) -> float:
        return self.profile.Ay * self.Fy_shear / (math.sqrt(3) * self.ym0)

    def check_shear_capacity_z(self) -> float:
        return self.force.Ved_z / self.shear_capacity_z()

    def check_shear_capacity_y(self) -> float:
        return self.force.Ved_y / self.shear_capacity_y()

    def check_total_shear(self) -> float:
        ur1 = self.check_shear_capacity_z()
        ur2 = self.check_shear_capacity_y()
        return max(ur1, ur2)

    def reduction_due_shear(self) -> float:
        if (
            self.force.Ved_y > self.shear_capacity_y() / 2
            or self.force.Ved_z > self.shear_capacity_z() / 2
        ):
            q_y = min(
                (((2 * self.force.Ved_y) / self.shear_capacity_y()) - 1) ** 2, 0.99
            )
            q_z = min(
                (((2 * self.force.Ved_z) / self.shear_capacity_z()) - 1) ** 2, 0.99
            )
            return min(q_y, q_z)

        else:
            return 0

    def tension_profile(self) -> float:
        return (self.profile.A * self.profile.Fy) / self.ym0

    def check_tension_profile(self) -> float:
        return self.force.Ned / self.tension_profile()

    def bending_capacity_profile_y(self) -> float:
        return self.Wply * self.profile.Fy / self.ym0

    def bending_capacity_profile_z(self) -> float:
        return self.Wply * self.profile.Fy / self.ym0

    def reduction_bending_capacity_factors(self) -> tuple[float, float]:
        n = self.force.Ned / self.tension_profile()
        aw = min(
            (self.profile.A - 2 * self.profile.B * self.profile.T) / self.profile.A, 0.5
        )
        af = min(
            (self.profile.A - 2 * self.profile.H * self.profile.T) / self.profile.A, 0.5
        )
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
        n = self.force.Ned / self.tension_profile()
        alpha = max(1.66 / (1 - (1.13 * (n**2))), 1)
        alpha = min(alpha, 6)

        beta = alpha

        ur = (self.force.Med_y / self.reduced_bending_capacity_y()) ** alpha + (
            self.force.Med_z / self.reduced_bending_capacity_y()
        ) ** beta
        return ur

    def check_interaction_axial_force_and_bending(self) -> float:
        ur = max(
            self.force.Med_y / self.reduced_bending_capacity_y(),
            self.force.Med_z / self.reduced_bending_capacity_z(),
            self.reduction_biaxial_bending_capacity(),
        )
        return ur

    def compression_capacity_y(self) -> float:
        return (
            self.profile.A
            * self.profile.Fy
            * self.buckling_factor.chi_reduction_factor_y
        ) / self.ym1

    def compression_capacity_z(self) -> float:
        return (
            self.profile.A
            * self.profile.Fy
            * self.buckling_factor.chi_reduction_factor_z
        ) / self.ym1

    def check_buckling_y(self) -> float:
        return self.force.Ned / self.compression_capacity_y()

    def check_buckling_z(self) -> float:
        return self.force.Ned / self.compression_capacity_z()

    def check_total_buckling(self) -> float:
        ur1 = self.check_buckling_z()
        ur2 = self.check_buckling_y()
        return max(ur1, ur2)

    def load_from_self_weight(self) -> float:
        return self.profile.G * 0.01 * si.kN / si.kg

    def bending_capacity_y(self) -> float:
        return self.profile.Wply * self.profile.Fy / self.ym1

    def check_bending_y(self) -> float:
        return self.force.Med_y / self.bending_capacity_y()

    def bending_capacity_z(self) -> float:
        return self.profile.Wplz * self.profile.Fy / self.ym1

    def check_bending_z(self) -> float:
        return self.force.Med_z / self.bending_capacity_z()

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
        if self.section_class < 3:
            fyy = min(self.buckling_factor.lambda_relative_slenderness_y() - 0.2, 0.8)
        else:
            fyy = min(self.buckling_factor.lambda_relative_slenderness_y() * 0.6, 0.6)
        kyy = self.Cmy() * (1 + fyy * ur_y)
        return kyy

    def kzz(self) -> float:
        ur_z = self.check_buckling_z()
        if self.section_class < 3:
            fzz = min(self.buckling_factor.lambda_relative_slenderness_z() - 0.2, 0.8)
        else:
            fzz = min(self.buckling_factor.lambda_relative_slenderness_z() * 0.6, 0.6)
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
        return (5 * self.load_from_self_weight() * self.profile.L**4) / (
            384 * self.E * self.profile.Iy
        )

    def deflection_bending_y(self) -> float:
        bending_moment = self.force.Med_y
        return (bending_moment * self.profile.L**2) / (8 * self.E * self.profile.Iy)

    def deflection_bending_z(self) -> float:
        bending_moment = self.force.Med_z
        return (bending_moment * self.profile.L**2) / (8 * self.E * self.profile.Iz)

    def check_deformation_y(self) -> float:
        limit = self.profile.L / self.limit_deformation
        if self.main_axis == "z":
            ur1 = (self.deflection_bending_y() + self.deflection_self_weight()) / limit
        else:
            ur1 = self.deflection_bending_y() / limit
        return ur1

    def check_deformation_z(self) -> float:
        limit = self.profile.L / self.limit_deformation
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

        return max(
            ur1,
            ur2,
            ur3,
        )

    def check_when_compressed_and_bended(self):
        ur1 = self.check_total_shear()
        ur2 = self.check_total_buckling()
        ur3 = self.check_total_bending()
        ur4 = self.check_interaction_buckling_and_bending()

        return max(
            ur1,
            ur2,
            ur3,
            ur4,
        )


if __name__ == "__main__":
    gammas = CountryFactors()
    gammas_country = gammas.finding_gammas("Sweden")
    steel = SteelGrade()
    steel_grade = steel.finding_steel("S355")

    profil = ProfileRhsToCalculation(
        type_profile='CF',
        sectional_area=18.36 * (10**2),
        height_profile=80,
        width_profile=60,
        thickness_flange=5,
        second_moment_area_y=271 * (10**4),
        second_moment_area_z=271 * (10**4),
        yield_strength=steel_grade,
        length=5,
        plastic_section_y=64.08 * (10**3),
        plastic_section_z=64.08 * (10**3),
        thickness_web=3,
        radius=4,
    )

    buckling = ReductionBucklingFactorsRHS(buckling_factor=1, profile=profil)

    # 80x60x5
    obiekt = CalculationRHS(
        sectional_axial_force=-50,
        sectional_bending_moment_y=5,
        sectional_bending_moment_z=0,
        sectional_shear_y=0,
        sectional_shear_z=0,
        eccentricity_y=0,
        eccentricity_z=0,
        gammas=gammas_country,
        limit_deformation=200,
        main_axis="z",
        profile=profil,
        buckling_factor=buckling,
    )

    print(
        # buckling.lambda_relative_slenderness_y(),
        # obiekt.compression_capacity_y(),
        # obiekt.check_total_buckling(),
        # obiekt.check_total_buckling(),
        # obiekt.bending_capacity_y(),
        # obiekt.check_bending_y(),
        # obiekt.reduced_bending_capacity_y(),
        # obiekt.kyy(),
        obiekt.check_class(),
        # obiekt.check_interaction_buckling_and_bending(),
        obiekt.check_tension_profile(),
        # obiekt.deflection_bending_y(),
    )
