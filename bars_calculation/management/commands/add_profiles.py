import json
import os
from typing import Dict, List

from django.core.management import BaseCommand

from bars_calculation.models import ProfileRhs

file_name = "RTRKKpro"


def reading_file(name: str) -> Dict:
    module_dir = os.path.dirname(__file__)
    two_levels_up = os.path.dirname(os.path.dirname(module_dir))
    folder = "static/bars_calculation"
    name = f"{folder}/{name}"
    file_path = os.path.join(two_levels_up, name)
    with open(f"{file_path}.json", "r") as file:
        data = json.load(file)
        return data


def cleaning_data(data: Dict) -> List:
    clear_profiles_squa = []
    for rows in data["body"]["data"]:
        if rows["@name"] == "Shape":
            for row in rows["row"]:
                if row['@NAME'] == 'SQUA':
                    clear_profiles_squa.append(row)
    return clear_profiles_squa


class Command(BaseCommand):
    def __convert_to_float(self, value) -> float:
        # try:
        return float(value.replace(',', '.'))
        # except ValueError:
        # return 0.0

    def handle(self, *args, **options):
        data = reading_file(file_name)
        profiles = cleaning_data(data)

        for profile in profiles:
            new_profile = ProfileRhs(
                name=profile['@NAME_REVIT'],
                H=int(profile["@DIM1"]),
                B=int(profile["@DIM2"]),
                T=self.__convert_to_float(profile["@DIM3"]),
                G=self.__convert_to_float(profile["@MASS"]),
                surf=self.__convert_to_float(profile["@SURF"]),
                r0=self.__convert_to_float(profile["@RS"]),
                r1=self.__convert_to_float(profile["@RA"]),
                A=self.__convert_to_float(profile["@SX"]),
                Ix=self.__convert_to_float(profile["@IX"]),
                Iy=self.__convert_to_float(profile["@IY"]),
                Iz=self.__convert_to_float(profile["@IZ"]),
                Wply=self.__convert_to_float(profile["@MSY"]),
                Wplz=self.__convert_to_float(profile["@MSZ"]),
            )
            new_profile.save()
        print("Profiles added")
