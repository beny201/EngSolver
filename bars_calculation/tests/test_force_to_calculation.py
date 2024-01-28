import forallpeople as si
import pytest

from ..calculation import ForceToCalculation, ProfileRhsToCalculation

si.environment('structural', top_level=False)


@pytest.fixture
def set_object():
    steel_grade = 355 * si.MPa

    main_axis_calc = "z"

    profile = ProfileRhsToCalculation(
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
        sectional_bending_moment_z=2,
        sectional_shear_y=10,
        sectional_shear_z=20,
        eccentricity_y=0,
        eccentricity_z=0,
        main_axis=main_axis_calc,
        profile=profile,
    )

    return force


class TestForceToCalculation:
    def test_should_return_axial_force_with_kN(self, set_object):
        expected_force = -50 * si.kN
        assert set_object.Ned_stress == expected_force

    def test_should_return_abs_axial_force_with_kN(self, set_object):
        expected_force = 50 * si.kN
        assert set_object.Ned == expected_force

    def test_should_return_Medy_with_kNm_and_self_weight(self, set_object):
        expected_force = 1453
        Med_y = set_object.total_bending_my().split()[0]
        assert Med_y == pytest.approx(expected_force, rel=2e-2)

    def test_should_return_Medz_with_kNm(self, set_object):
        expected_force = 2 * si.kN * si.m
        assert set_object.Med_z == expected_force

    def test_should_return_Vedz_with_kN(self, set_object):
        expected_force = 20 * si.kN
        assert set_object.Ved_z == expected_force

    def test_should_return_Vedy_with_kN(self, set_object):
        expected_force = 10 * si.kN
        assert set_object.Ved_y == expected_force

    def test_should_return_bending_from_eccentricity_y_with_dl(
        self, set_object, mocker
    ):
        mock_data = 10 * si.mm
        mocker.patch.object(set_object, 'ecc_z', mock_data)
        expected_force = 1453 + 500
        Med_y = set_object.total_bending_my().split()[0]
        assert Med_y == pytest.approx(expected_force, rel=2e-2)

    def test_should_return_bending_bending_from_eccentricity_z(
        self, set_object, mocker
    ):
        mock_data = 10 * si.mm
        mocker.patch.object(set_object, 'ecc_y', mock_data)
        expected_force = 2500
        expected_Med_y = set_object.total_bending_mz().split()[0]
        assert expected_Med_y == pytest.approx(expected_force, rel=2e-2)

    def test_should_return_bending_from_eccentricity_y_without_dl(
        self, set_object, mocker
    ):
        mock_data = "y"
        mocker.patch.object(set_object, 'main_axis', mock_data)
        expected_force = 1000
        Med_y = set_object.total_bending_my().split()[0]
        assert Med_y == pytest.approx(expected_force, rel=2e-2)
