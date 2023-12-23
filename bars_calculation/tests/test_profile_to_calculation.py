import forallpeople as si
import pytest

from ..calculation import ProfileRhsToCalculation

si.environment('structural', top_level=False)
cm = si.m / 100


@pytest.fixture
def set_object():
    steel_grade = 355 * si.MPa

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

    return profile


class TestProfileToCalculationClass:
    def test_should_return_radius_of_gyration_iy(self, set_object):
        iy = set_object.radius_of_gyration_iy().split()[0]
        expected = 0.0459
        assert expected == pytest.approx(iy, rel=2e-2)

    def test_should_return_radius_of_gyration_iz(self, set_object):
        iz = set_object.radius_of_gyration_iz().split()[0]
        expected = 0.0399
        assert expected == pytest.approx(iz, rel=2e-2)

    def test_should_return_shear_area_z(self, set_object):
        az = set_object.shear_area_z().split()[0]
        expected = 0.0009
        assert expected == pytest.approx(az, rel=2e-2)

    def test_should_return_shear_area_y(self, set_object):
        ay = set_object.shear_area_y().split()[0]
        expected = 0.00075
        assert expected == pytest.approx(ay, rel=2e-2)

    def test_should_return_elastic_section_y(self, set_object):
        wely = set_object.elastic_section_y().split()[0]
        expected = 0.000058
        assert expected == pytest.approx(wely, rel=2e-2)

    def test_should_return_elastic_section_z(self, set_object):
        welz = set_object.elastic_section_z().split()[0]
        expected = 0.0000526
        assert expected == pytest.approx(welz, rel=2e-2)

    @pytest.mark.parametrize(
        "steel_grade, expected", [(235 * si.MPa, 1), (275 * si.MPa, 0.92)]
    )
    def test_should_return_epsilon(self, set_object, steel_grade, expected):
        set_object.Fy = steel_grade
        epsilon = set_object.check_epsilon()
        assert expected == pytest.approx(epsilon, rel=2e-2)
