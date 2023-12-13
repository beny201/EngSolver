from typing import Dict

import forallpeople as si

si.environment('structural', top_level=False)

cm = si.m / 100


class CountryFactors:
    COUNTRY_FACTORS: Dict[str, Dict[str, int]] = {
        'Norway': {'ym0': 1.05, 'ym1': 1.05, 'ym2': 1.25},
        'Sweden': {'ym0': 1.00, 'ym1': 1.00, 'ym2': 1.25},
        'Denmark': {'ym0': 1.10, 'ym1': 1.20, 'ym2': 1.35},
        'Germany': {'ym0': 1.00, 'ym1': 1.10, 'ym2': 1.25},
    }

    def finding_gammas(self, country: str) -> Dict[str, float]:
        for key, values in self.COUNTRY_FACTORS.items():
            if country in key:
                return self.COUNTRY_FACTORS[key]


class SteelGrade:
    MODULUS_OF_ELASTICITY = 210_000 * si.MPa
    WEIGHT = 7900 * si.kg / si.m**3

    STEEL_GRADE = {
        'S235': 235 * si.MPa,
        'S275': 275 * si.MPa,
        'S355': 355 * si.MPa,
    }

    def finding_steel(self, steel: str) -> int:
        for key, values in self.STEEL_GRADE.items():
            if steel in key:
                return self.STEEL_GRADE[steel]


class BucklingCurves:
    BUCKLING_CURVES: Dict[str, int] = {
        'a0': 0.13,
        'a': 0.21,
        'b': 0.34,
        'c': 0.49,
        'd': 0.76,
    }

    BUCKLING_types: Dict[str, str] = {'CF': "c", 'HF': "a"}

    def chosen_type_profile(self, type_of_profile: str) -> str:
        for key, value in self.BUCKLING_types.items():
            if type_of_profile in key:
                return self.BUCKLING_types[type_of_profile]
        print("Check profile")

    def buckling_curve(self, buckling_curve: str) -> float:
        for key, value in self.BUCKLING_CURVES.items():
            if buckling_curve in key:
                return self.BUCKLING_CURVES[buckling_curve]
        print("Check chosen curve")
