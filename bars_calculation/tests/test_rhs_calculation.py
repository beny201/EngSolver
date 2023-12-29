import forallpeople as si
import pytest

from ..calculation import (
    CalculationRHS,
    CountryFactors,
    CrossSectionClass,
    ForceToCalculation,
    ProfileRhsToCalculation,
    ReductionBucklingFactorsRHS,
)

si.environment('structural', top_level=False)
cm = si.m / 100


# is there way to make it simpler ? i tried to use wraped function but normal test do not pass. To ask
@pytest.fixture
def profile():
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


@pytest.fixture
def force(profile):
    main_axis_calc = "z"
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


@pytest.fixture
def force_2(profile):
    main_axis_calc = "z"
    force = ForceToCalculation(
        sectional_axial_force=-50,
        sectional_bending_moment_y=1,
        sectional_bending_moment_z=2,
        sectional_shear_y=100,
        sectional_shear_z=120,
        eccentricity_y=0,
        eccentricity_z=0,
        main_axis=main_axis_calc,
        profile=profile,
    )
    return force


@pytest.fixture
def set_object(force, profile):
    main_axis_calc = "z"
    buckling_factor = 1
    country = "Sweden"
    limit_deformation = 200

    gammas = CountryFactors()
    used_gammas = gammas.finding_gammas(country)

    section_class = CrossSectionClass(
        main_axis="z",
        sectional_force=force,
        profile=profile,
    )
    used_profile_class = section_class.check_class()

    buckling_factor_to_calculate = ReductionBucklingFactorsRHS(
        buckling_factor=buckling_factor, profile=profile
    )

    calculation = CalculationRHS(
        sectional_forces=force,
        gammas=used_gammas,
        limit_deformation=limit_deformation,
        main_axis=main_axis_calc,
        profile=profile,
        buckling_factor=buckling_factor_to_calculate,
        section_class=used_profile_class,
    )

    return calculation


@pytest.fixture
def set_object_2(force_2, profile):
    main_axis_calc = "z"
    buckling_factor = 1
    country = "Sweden"
    limit_deformation = 200

    gammas = CountryFactors()
    used_gammas = gammas.finding_gammas(country)

    section_class = CrossSectionClass(
        main_axis="z",
        sectional_force=force_2,
        profile=profile,
    )
    used_profile_class = section_class.check_class()

    buckling_factor_to_calculate = ReductionBucklingFactorsRHS(
        buckling_factor=buckling_factor, profile=profile
    )

    calculation = CalculationRHS(
        sectional_forces=force_2,
        gammas=used_gammas,
        limit_deformation=limit_deformation,
        main_axis=main_axis_calc,
        profile=profile,
        buckling_factor=buckling_factor_to_calculate,
        section_class=used_profile_class,
    )

    return calculation


class TestCalculationRHSClass:
    def test_should_prove_that_Wply_was_used(self, set_object):
        tested = set_object.Wply
        expected = set_object.profile.Wply
        assert tested == expected

    def test_should_prove_that_Wely_was_used(self, set_object):
        set_object.section_class = 3
        tested = set_object.switching_to_Wely()
        expected = set_object.profile.Wely
        assert tested == expected

    def test_should_prove_that_Wplz_was_used(self, set_object):
        tested = set_object.Wplz
        expected = set_object.profile.Wplz
        assert tested == expected

    def test_should_prove_that_Welz_was_used(self, set_object):
        set_object.section_class = 3
        tested = set_object.switching_to_Welz()
        expected = set_object.profile.Welz
        assert tested == expected

    def test_should_return_shear_capacity_z(self, set_object):
        tested = set_object.shear_capacity_z().split()[0]
        expected = 185000
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_shear_capacity_y(self, set_object):
        tested = set_object.shear_capacity_y().split()[0]
        expected = 154185
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_shear_y_ur(self, set_object):
        tested = set_object.check_shear_capacity_y()
        expected = 0.064
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_shear_z_ur(self, set_object):
        tested = set_object.check_shear_capacity_z()
        expected = 0.108
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_total_shear_ur(self, set_object):
        tested = set_object.check_total_shear()
        expected = 0.108
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_total_value_of_reduction_due_shear(self, set_object):
        tested = set_object.reduction_due_shear()
        expected = 0
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_total_value_of_reduction_due_shear_when_Ved_exceeded(
        self, set_object
    ):
        set_object.force.Ved_z = 100 * si.kN
        reduction = set_object.reduction_due_shear()
        expected = 0.0065
        assert reduction == pytest.approx(expected, rel=2e-2)

    def test_should_return_tension_profile(self, set_object):
        tested = set_object.tension_profile().split()[0]
        expected = 587525
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_tension_ur(self, set_object):
        tested = set_object.check_tension_profile()
        expected = 0.0851
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_bending_capacity_y(self, set_object):
        tested = set_object.bending_capacity_profile_y().split()[0]
        expected = 24512
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_bending_capacity_z(self, set_object):
        tested = set_object.bending_capacity_profile_z().split()[0]
        expected = 21650
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_reduction_bending_capacity_factors(self, set_object):
        tested = set_object.reduction_bending_capacity_factors()
        expected = (1.22, 1.158)
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_not_reduced_bending_capacity_y(self, set_object):
        tested = set_object.reduced_bending_capacity_y()
        expected = set_object.bending_capacity_profile_y()
        assert tested == expected

    def test_should_return_reduced_bending_capacity_y(self, set_object, mocker):
        mocker.patch.object(
            set_object, 'reduction_bending_capacity_factors', return_value=(0.8, 0.9)
        )
        tested = set_object.reduced_bending_capacity_y()
        expected = 0.8 * set_object.bending_capacity_profile_y()
        assert tested == expected

    def test_should_return_not_reduced_bending_capacity_z(self, set_object):
        tested = set_object.reduced_bending_capacity_z()
        expected = set_object.bending_capacity_profile_z()
        assert tested == expected

    def test_should_return_reduced_bending_capacity_z(self, set_object, mocker):
        mocker.patch.object(
            set_object, 'reduction_bending_capacity_factors', return_value=(0.8, 0.9)
        )
        tested = set_object.reduced_bending_capacity_z()
        expected = 0.9 * set_object.bending_capacity_profile_z()
        assert tested == expected

    def test_should_return_reduced_biaxial_bending_capacity(self, set_object):
        tested = set_object.reduction_biaxial_bending_capacity()
        expected = 0.0234
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_check_interaction_axial_force_and_bending(self, set_object):
        tested = set_object.check_interaction_axial_force_and_bending()
        expected = 0.0923
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_compression_capacity_y(self, set_object):
        tested = set_object.compression_capacity_y().split()[0]
        expected = 199395
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_compression_capacity_z(self, set_object):
        tested = set_object.compression_capacity_z().split()[0]
        expected = 160269
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_ur_buckling_y(self, set_object):
        tested = set_object.check_buckling_y()
        expected = 0.25
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_ur_buckling_z(self, set_object):
        tested = set_object.check_buckling_z()
        expected = 0.31
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_total_buckling(self, set_object):
        tested = set_object.check_total_buckling()
        expected = 0.31
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_bending_capacity_y_(self, set_object):
        tested = set_object.bending_capacity_y().split()[0]
        expected = 24512
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_bending_capacity_y_with_reduction_of_shear(
        self, set_object_2
    ):
        tested = set_object_2.bending_capacity_y().split()[0]
        expected = 22348
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_bending_y(self, set_object):
        tested = set_object.check_bending_y()
        expected = 0.057
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_bending_capacity_z_(self, set_object):
        tested = set_object.bending_capacity_z().split()[0]
        expected = 21647
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_bending_capacity_z_with_reduction_of_shear(
        self, set_object_2
    ):
        tested = set_object_2.bending_capacity_z().split()[0]
        expected = 19736
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_bending_z(self, set_object):
        tested = set_object.check_bending_z()
        expected = 0.092
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_total_bending(self, set_object):
        tested = set_object.check_total_bending()
        expected = 0.092
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_Cmy(self, set_object):
        tested = set_object.Cmy()
        expected = 0.95
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_kyy(self, set_object):
        tested = set_object.kyy()
        expected = 1.140
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_kyy_when_sc_3(self, set_object, mocker):
        mocker.patch.object(set_object, 'section_class', 3)
        tested = set_object.kyy()
        expected = 1.09
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_kzz(self, set_object):
        tested = set_object.kzz()
        expected = 1.187
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_kzz_when_sc_3(self, set_object, mocker):
        mocker.patch.object(set_object, 'section_class', 3)
        tested = set_object.kzz()
        expected = 1.127
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_kzy(self, set_object):
        tested = set_object.kzy()
        expected = 0.684
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_interaction_buckling_and_bending(self, set_object):
        tested = set_object.check_interaction_buckling_and_bending()
        expected = 0.461
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_deflection_self_weight(self, set_object):
        tested = set_object.deflection_self_weight().split()[0]
        expected = 0.00145
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_deflection_bending_y(self, set_object):
        tested = set_object.deflection_bending_y().split()[0]
        expected = 0.006
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_return_deflection_bending_z(self, set_object):
        tested = set_object.deflection_bending_z().split()[0]
        expected = 0.0113
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_deformation_y_main_axis_z(self, set_object):
        tested = set_object.check_deformation_y()
        expected = 0.299
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_deformation_y_main_axis_y(self, set_object, mocker):
        mocker.patch.object(set_object, 'main_axis', "y")
        tested = set_object.check_deformation_y()
        expected = 0.241
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_deformation_z_main_axis_z(self, set_object):
        tested = set_object.check_deformation_z()
        expected = 0.45
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_deformation_z_main_axis_y(self, set_object, mocker):
        mocker.patch.object(set_object, 'main_axis', "y")
        tested = set_object.check_deformation_z()
        expected = 0.51
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_deformation(self, set_object):
        tested = set_object.check_deformation()
        expected = 0.45
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_when_tensioned_and_bended(self, set_object):
        tested = set_object.check_when_tensioned_and_bended()
        expected = 0.108
        assert tested == pytest.approx(expected, rel=2e-2)

    def test_should_check_when_compressed_and_bended(self, set_object):
        tested = set_object.check_when_compressed_and_bended()
        expected = 0.461
        assert tested == pytest.approx(expected, rel=2e-2)
