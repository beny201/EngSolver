import math

import forallpeople as si

from .profile_to_calculation import ProfileRhsToCalculation
from .structural_parameters import BucklingCurves, SteelGrade

si.environment('structural', top_level=False)

cm = si.m / 100


class ReductionBucklingFactorsRHS:
    def __init__(self, buckling_factor: float, profile: ProfileRhsToCalculation):
        self.buckling_factor = buckling_factor
        self.curve_for_chosen_profile = BucklingCurves().chosen_type_profile(
            profile.type_profile
        )
        self.buckling_curve = BucklingCurves().buckling_curve(
            self.curve_for_chosen_profile
        )
        self.E = SteelGrade().MODULUS_OF_ELASTICITY
        self.profile = profile
        self.epsilon = self.profile.epsilon
        self.buckling_length = self.buckling_length()
        self.lambda_slenderness_1 = self.lambda_slenderness_1()
        self.chi_reduction_factor_y = self.chi_reduction_factor_y()
        self.chi_reduction_factor_z = self.chi_reduction_factor_z()

    def lambda_slenderness_1(self) -> float:
        return math.pi * (math.sqrt((self.E / self.profile.Fy)))

    def buckling_length(self) -> float:
        return self.profile.L * self.buckling_factor

    def lambda_relative_slenderness_y(self) -> float:
        return (self.buckling_length / self.profile.iy) * (
            1 / self.lambda_slenderness_1
        )

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
        return (self.buckling_length / self.profile.iz) * (
            1 / self.lambda_slenderness_1
        )

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
