import math
from typing import Any, Union

import forallpeople as si

from .force_to_calculation import ForceToCalculation
from .profile_to_calculation import ProfileRhsToCalculation
from .structural_parameters import SteelGrade

# from bars_calculation.calculation import ForceToCalculation, ProfileRhsToCalculation, SteelGrade

si.environment('structural', top_level=False)

cm = si.m / 100


class CrossSectionClass:
    def __init__(
        self,
        main_axis: str,
        sectional_force: ForceToCalculation,
        profile: ProfileRhsToCalculation,
    ):
        self.profile = profile
        self.force = sectional_force
        self.main_axis = main_axis
        self.alpha, self.psi = self.stresses_web_alpha()

        self.class_section_compression = {
            1: 33 * self.profile.epsilon,
            2: 38 * self.profile.epsilon,
            3: 42 * self.profile.epsilon,
        }

        self.class_section_bending_compression = {
            1: {
                (0, 0.5): (396 * self.profile.epsilon) / (13 * self.alpha - 1),
                (0.5, 1): (36 * self.profile.epsilon) / self.alpha,
            },
            2: {
                (0, 5): (456 * self.profile.epsilon) / (13 * self.alpha - 1),
                (0.5, 1): (41.5 * self.profile.epsilon) / self.alpha,
            },
        }
        self.class_section_bending_compression_3 = {
            3: {
                (-1, 2): (42 * self.profile.epsilon) / (0.67 + 0.33 * self.psi),
                (-1, 3): (62 * self.profile.epsilon)
                * (1 - self.psi)
                * math.sqrt(abs(self.psi)),
            }
        }

    def stresses_web_alpha(self) -> Union[Any, Any]:
        Ga = self.force.Ned_stress / self.profile.A
        Gy = self.force.Med_y / self.profile.Wely
        Gz = self.force.Med_z / self.profile.Welz

        G_1 = Ga - Gy - Gz
        G_2 = Ga + Gy + Gz

        alpha = (G_1 * self.profile.H) / (G_1 - G_2) / self.profile.H
        psi = G_2 / G_1

        return alpha, psi

    def c_t_flange(self) -> float:
        c_t = (
            self.profile.B - 2 * self.profile.T - 2 * self.profile.R
        ) / self.profile.T
        return c_t

    def c_t_web(self) -> float:
        c_t = (
            self.profile.H - 2 * self.profile.T - 2 * self.profile.R
        ) / self.profile.T
        return c_t

    def web_compression_classification_class(self) -> int:
        c_t = self.c_t_web()

        if self.alpha < 0:
            return 1
        elif self.alpha >= 1:
            for class_section, limit in self.class_section_compression.items():
                if c_t <= limit:
                    return class_section

        for class_section, limits in self.class_section_bending_compression.items():
            for value, formulas in limits.items():
                if value[0] < self.alpha < value[1]:
                    if c_t <= formulas:
                        return class_section

        for class_section, limits in self.class_section_bending_compression_3.items():
            for value, formulas in limits.items():
                if self.psi > value[0]:
                    if c_t <= formulas:
                        return class_section
                elif self.psi <= value[0]:
                    if c_t <= formulas:
                        return class_section
        return 4

    def flange_check_class(self) -> int:
        c_t = self.c_t_flange()
        for class_section, limit in self.class_section_compression.items():
            if c_t <= limit:
                return class_section
        return 4

    def check_class(self) -> int:
        web = self.web_compression_classification_class()
        if self.force.Ned_stress < 0:
            flange = self.flange_check_class()
            return max(web, flange)
        return web


if __name__ == "__main__":
    steel = SteelGrade()
    steel_grade = steel.finding_steel("S355")

    profil = ProfileRhsToCalculation(
        type_profile='CF',
        sectional_area=18.36 * (10**2),
        height_profile=120,
        width_profile=120,
        thickness_flange=4,
        second_moment_area_y=271 * (10**4),
        second_moment_area_z=271 * (10**4),
        yield_strength=steel_grade,
        length=5,
        plastic_section_y=64.08 * (10**3),
        plastic_section_z=64.08 * (10**3),
        radius=4,
    )

    force = ForceToCalculation(
        sectional_axial_force=-50,
        sectional_bending_moment_y=1,
        sectional_bending_moment_z=0,
        sectional_shear_y=0,
        sectional_shear_z=0,
        eccentricity_y=0,
        eccentricity_z=0,
        main_axis="z",
        profile=profil,
    )

    obiekt = CrossSectionClass(
        main_axis="z",
        force=force,
        profile=profil,
    )

    print(
        obiekt.check_class(),
    )
