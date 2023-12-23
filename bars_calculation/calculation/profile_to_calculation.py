import math
from typing import Union

import forallpeople as si

from .structural_parameters import SteelGrade

si.environment('structural', top_level=False)

cm = si.m / 100


class ProfileRhsToCalculation:
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
        radius: float,
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
        self.iy = self.radius_of_gyration_iy()
        self.iz = self.radius_of_gyration_iz()
        self.Az = self.shear_area_z()
        self.Ay = self.shear_area_y()
        self.G = self.weight_per_m()
        self.Wely = self.elastic_section_y()
        self.Welz = self.elastic_section_z()
        self.R = radius * si.mm
        self.epsilon = self.check_epsilon()

    def weight_per_m(self) -> float:
        return self.A * SteelGrade().WEIGHT

    def radius_of_gyration_iy(self) -> float:
        iy = self.Iy / self.A
        return math.sqrt(iy) * si.mm

    def radius_of_gyration_iz(self) -> float:
        iz = self.Iz / self.A
        return math.sqrt(iz) * si.mm

    def shear_area_z(self) -> float:
        Az = (self.A * self.H) / (self.B + self.H)
        return Az

    def shear_area_y(self) -> float:
        Ay = (self.A * self.B) / (self.B + self.H)
        return Ay

    def elastic_section_y(self) -> float:
        Wely = self.Iy / (self.H / 2)
        return Wely

    def elastic_section_z(self) -> float:
        Welz = self.Iz / (self.B / 2)
        return Welz

    def check_epsilon(self) -> float:
        yield_strength = self.Fy / si.MPa
        return math.sqrt(235 / yield_strength)
