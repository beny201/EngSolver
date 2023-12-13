import pytest

from ..calculation import CountryFactors


@pytest.mark.parametrize(
    "txt, expected",
    [
        ("Norway", {'ym0': 1.05, 'ym1': 1.05, 'ym2': 1.25}),
        ("Germany", {'ym0': 1.00, 'ym1': 1.10, 'ym2': 1.25}),
    ],
)
def test_should_return_dic_with_factors_for_countires(txt, expected):
    factor_object = CountryFactors()
    assert factor_object.finding_gammas(txt) == expected
