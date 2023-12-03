from typing import Union

import forallpeople as si

from .profile_to_calculation import ProfileRhsToCalculation

si.environment('structural', top_level=False)

cm = si.m / 100


class ForceToCalculation:
    def __init__(
        self,
        sectional_axial_force: Union[int, float],
        sectional_bending_moment_y: Union[int, float],
        sectional_bending_moment_z: Union[int, float],
        sectional_shear_y: Union[int, float],
        sectional_shear_z: Union[int, float],
        eccentricity_y: Union[int, float],
        eccentricity_z: Union[int, float],
        main_axis: str,
        profile: ProfileRhsToCalculation,
    ):
        self.profile = profile
        self.main_axis = main_axis
        self.Ned = abs(sectional_axial_force) * si.kN
        self.Med_y = sectional_bending_moment_y * si.kN * si.m
        self.Med_z = sectional_bending_moment_z * si.kN * si.m
        self.Ved_z = sectional_shear_z * si.kN
        self.Ved_y = sectional_shear_y * si.kN
        self.ecc_y = eccentricity_y * si.mm
        self.ecc_z = eccentricity_z * si.mm
        self.Ned_stress = sectional_axial_force * si.kN
        self.Med_y = self.total_bending_my()
        self.Med_z = self.total_bending_mz()

    def load_from_self_weight(self) -> float:
        return self.profile.G * 0.01 * si.kN / si.kg

    def bending_from_self_weight(self) -> float:
        return (self.load_from_self_weight() * self.profile.L**2) / 8

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
