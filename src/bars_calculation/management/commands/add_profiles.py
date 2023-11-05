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
    def handle(self, *args, **options):
        data = reading_file(file_name)
        profiles = cleaning_data(data)[:2]

        for profile in profiles:
            new_profile = ProfileRhs(
                name=profile['@NAME1'],
                H=int(profile["@DIM1"]),
                B=int(profile["@DIM2"]),
                T=float(profile["@DIM3"].replace(",", ".")),
                G=float(profile["@MASS"].replace(",", ".")),
                surf=float(profile["@SURF"].replace(",", ".")),
                r0=float(profile["@RS"].replace(",", ".")),
                r1=float(profile["@RA"].replace(",", ".")),
                A=float(profile["@SX"].replace(",", ".")),
                Iy=float(profile["@IY"].replace(",", ".")),
                Iz=float(profile["@IZ"].replace(",", ".")),
                Wply=float(profile["@MSY"].replace(",", ".")),
                Wplz=float(profile["@MSZ"].replace(",", ".")),
            )
            new_profile.save()
        print("Profiles added")
