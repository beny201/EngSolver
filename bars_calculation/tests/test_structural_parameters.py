import forallpeople as si
import pytest

from ..calculation import BucklingCurves, CountryFactors, SteelGrade

si.environment('structural', top_level=False)


@pytest.mark.parametrize(
    "txt, expected",
    [
        ("Norway", {'ym0': 1.05, 'ym1': 1.05, 'ym2': 1.25}),
        ("Germany", {'ym0': 1.00, 'ym1': 1.10, 'ym2': 1.25}),
    ],
)
def test_should_return_dic_with_factors_for_countries(txt, expected):
    factor_object = CountryFactors()
    assert factor_object.finding_gammas(txt) == expected


@pytest.mark.parametrize(
    "txt, expected",
    [
        ("S235", 235 * si.MPa),
        ("S355", 355 * si.MPa),
    ],
)
def test_should_return_steel_grade_for_chose_type(txt, expected):
    steel_object = SteelGrade()
    assert steel_object.finding_steel(txt) == expected


@pytest.mark.parametrize(
    "txt, expected",
    [
        ("CF", 'c'),
        ("HF", 'a'),
    ],
)
def test_should_return_buckling_curve_for_chosen_type_of_profile(txt, expected):
    steel_object = BucklingCurves()
    assert steel_object.chosen_type_profile(txt) == expected


@pytest.mark.parametrize(
    "txt, expected",
    [
        ("a", 0.21),
        ("d", 0.76),
    ],
)
def test_should_return_value_for_buckling_curve(txt, expected):
    steel_object = BucklingCurves()
    assert steel_object.buckling_curve(txt) == expected
