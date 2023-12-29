import forallpeople as si
import pytest

from ..calculation import CrossSectionClass, ForceToCalculation, ProfileRhsToCalculation

si.environment('structural', top_level=False)
cm = si.m / 100


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
        sectional_bending_moment_z=0,
        sectional_shear_y=0,
        sectional_shear_z=0,
        eccentricity_y=0,
        eccentricity_z=0,
        main_axis=main_axis_calc,
        profile=profile,
    )

    check_section = CrossSectionClass(main_axis_calc, force, profile)
    return check_section


class TestProfileClass:
    def test_should_return_factor_alpha_psi(self, set_object):
        alpha, psi = set_object.stresses_web_alpha()
        expected_alpha = 0.92
        expected_psi = -0.083
        assert alpha == pytest.approx(expected_alpha, abs=2e-2)
        assert psi == pytest.approx(expected_psi, abs=2e-2)

    def test_should_return_c_t_flange(self, set_object):
        c_t = set_object.c_t_flange()
        expected = 26
        assert c_t == pytest.approx(expected, abs=2e-2)

    def test_should_return_c_t_web(self, set_object):
        c_t = set_object.c_t_web()
        expected = 26
        assert c_t == pytest.approx(expected, abs=2e-2)

    def test_should_return_web_class(self, set_object):
        web_class = set_object.web_compression_classification_class()
        expected = 1
        assert web_class == expected

    @pytest.mark.parametrize("mock_data, expected", [(-2, 1)])
    def test_should_return_web_class_with_mocker_alpha(
        self, set_object, mocker, mock_data, expected
    ):
        mocker.patch.object(set_object, 'alpha', mock_data)
        web_class = set_object.web_compression_classification_class()
        assert web_class == expected

    @pytest.mark.parametrize("mock_data, expected", [(40, 3), (30, 1), (35, 2)])
    def test_should_return_web_class_with_mocker_c_t(
        self, set_object, mocker, mock_data, expected
    ):
        mocker.patch.object(set_object, 'c_t_web', return_value=mock_data)
        web_class = set_object.web_compression_classification_class()
        assert web_class == expected

    @pytest.mark.parametrize("mock_data, expected", [(50, 4), (10, 1), (30, 2)])
    def test_should_return_flange_class_with_mocker(
        self, set_object, mocker, mock_data, expected
    ):
        mocker.patch.object(set_object, 'c_t_flange', return_value=mock_data)
        flange_class = set_object.flange_check_class()
        assert flange_class == expected

    def test_should_return_flange_class(self, set_object):
        flange_class = set_object.flange_check_class()
        expected = 1
        assert flange_class == expected

    def test_should_return_class_profile(self, set_object):
        object_class = set_object.check_class()
        expected = 1
        assert object_class == expected

    @pytest.mark.parametrize("mock_data, expected", [(1, 1), (3, 3)])
    def test_should_return_class_profile_with_mocker(
        self, set_object, mocker, mock_data, expected
    ):
        mocker.patch.object(
            set_object, 'web_compression_classification_class', return_value=mock_data
        )
        mocker.patch.object(set_object, 'flange_check_class', return_value=mock_data)
        object_class = set_object.check_class()
        assert object_class == expected
