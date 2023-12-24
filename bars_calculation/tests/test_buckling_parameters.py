import forallpeople as si
import pytest

from ..calculation import ProfileRhsToCalculation, ReductionBucklingFactorsRHS

si.environment('structural', top_level=False)
cm = si.m / 100


@pytest.fixture
def set_object():
    steel_grade = 355 * si.MPa
    buckling_factor = 2

    profile = ProfileRhsToCalculation(
        type_profile='CF',
        sectional_area=16.55 * (10**2),
        height_profile=120,
        width_profile=100,
        thickness_flange=4,
        second_moment_area_y=348 * (10**4),
        second_moment_area_z=263 * (10**4),
        yield_strength=steel_grade,
        length=5,
        plastic_section_y=69.05 * (10**3),
        plastic_section_z=60.98 * (10**3),
        radius=4,
    )

    reduction = ReductionBucklingFactorsRHS(buckling_factor, profile)

    return reduction


class TestBucklingParametersClass:
    def test_should_return_lambda_slenderness_1(self, set_object):
        tested_parameter = set_object.lambda_slenderness_1
        expected = 76.4
        assert expected == pytest.approx(tested_parameter, rel=2e-2)

    def test_should_return_buckling_length(self, set_object):
        expected = 10 * si.m
        assert expected == set_object.buckling_length

    def test_should_return_lambda_relative_slenderness_y(self, set_object):
        tested_parameter = set_object.lambda_relative_slenderness_y()
        expected = 2.85
        assert expected == pytest.approx(tested_parameter, rel=2e-2)

    def test_should_return_lambda_relative_slenderness_z(self, set_object):
        tested_parameter = set_object.lambda_relative_slenderness_z()
        expected = 3.28
        assert expected == pytest.approx(tested_parameter, rel=2e-2)

    def test_should_return_theta_reduction_factor_y(self, set_object):
        tested_parameter = set_object.theta_reduction_factor_y()
        expected = 5.22
        assert expected == pytest.approx(tested_parameter, rel=2e-2)

    def test_should_return_theta_reduction_factor_z(self, set_object):
        tested_parameter = set_object.theta_reduction_factor_z()
        expected = 6.58
        assert expected == pytest.approx(tested_parameter, rel=2e-2)

    def test_should_return_chi_reduction_factor_y(self, set_object):
        tested_parameter = set_object.chi_reduction_factor_y
        expected = 0.106
        assert expected == pytest.approx(tested_parameter, rel=2e-2)

    def test_should_return_chi_reduction_factor_z(self, set_object):
        tested_parameter = set_object.chi_reduction_factor_z
        expected = 0.081
        assert expected == pytest.approx(tested_parameter, rel=2e-2)
