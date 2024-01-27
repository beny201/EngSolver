import json
import os
from typing import Dict, List, Tuple

from django.core.management.base import BaseCommand

from ...models import Bolt, BoltStandard, Nut, NutStandard, Washer, WasherStandard

file_name_bolt = ["bolts_8_8", "bolts_10_9"]

BOLTS_STANDARDS = {
    "8_8": ["EN-ISO-4032", "EN-ISO-4014", "EN-ISO-7089"],
    "10_9": ["14399-4D", "14399-4", "14399-5", "14399-6"],
}

_NUT_STANDARDS_ = [
    "EN-ISO-4032",
    "14399-4D",
]
_WASHER_STANDARDS_ = ['EN-ISO-7089', "14399-6", '14399-5']
_BOLTS_STANDARDS_ = ['14399-4', "EN-ISO-4014"]


def reading_file(name: str) -> Dict:
    module_dir = os.path.dirname(__file__)
    two_levels_up = os.path.dirname(os.path.dirname(module_dir))
    folder = "static/distance_checker"
    name = f"{folder}/{name}"
    file_path = os.path.join(two_levels_up, name)
    with open(f"{file_path}.txt", "r") as file:
        data = json.load(file)
        return data


def cleaning_data(bolts: Dict, bolt_grade: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    used_standard = BOLTS_STANDARDS[bolt_grade]

    cleaned_data_bolt = []
    cleaned_data_nut = []
    cleaned_data_washer = []
    for bolt in bolts["Bolts"]:
        if bolt["din"] == used_standard[0]:
            cleaned_data_nut.append(bolt)
        elif bolt["din"] == used_standard[1]:
            cleaned_data_bolt.append(bolt)
        elif bolt["din"] == used_standard[2]:
            cleaned_data_washer.append(bolt)
        elif used_standard[3]:
            if bolt["din"] == used_standard[3]:
                cleaned_data_washer.append(bolt)

    return cleaned_data_bolt, cleaned_data_nut, cleaned_data_washer


class Command(BaseCommand):
    def handle(self, *args, **options):
        for nut in _NUT_STANDARDS_:
            NutStandard(title=nut).save()

        for washer in _WASHER_STANDARDS_:
            WasherStandard(title=washer).save()

        for bolt in _BOLTS_STANDARDS_:
            BoltStandard(title=bolt).save()

        print("All standard were added")

        for file in file_name_bolt:
            data = reading_file(file)

            if file == "bolts_10_9":
                bolt_grade = "10_9"
            else:
                bolt_grade = "8_8"

            bolts = cleaning_data(data, bolt_grade)[0]
            bolts_standard = bolts[0]["din"]
            used_standard = BoltStandard.objects.get(title=bolts_standard)

            for bolt in bolts:
                new_bolt = Bolt(
                    name=bolt["name"],
                    thickness_bolt_head=float(bolt["p1"]),
                    width_bolt_head=float(bolt["p4"]),
                    length=int(bolt["length"]),
                    diameter=int(bolt["diameter"]),
                    thread_length=float(bolt["p2"]),
                    standard=used_standard,
                )
                new_bolt.save()

            nuts = cleaning_data(data, bolt_grade)[1]
            nut_standard = nuts[0]["din"]

            used_standard = NutStandard.objects.get(title=nut_standard)
            for nut in nuts:
                new_nut = Nut(
                    name=nut["name"],
                    thickness_nut=float(nut["p1"]),
                    width_nut=float(nut["p4"]),
                    diameter=int(nut["diameter"]),
                    standard=used_standard,
                )
                new_nut.save()

            washers = cleaning_data(data, bolt_grade)[2]
            washer_standard = washers[0]["din"]

            used_standard = WasherStandard.objects.get(title=washer_standard)
            for washer in washers:
                new_washer = Washer(
                    name=washer["name"],
                    thickness_washer=float(washer["p1"]),
                    width_washer=float(washer["p4"]),
                    diameter=int(washer["diameter"]),
                    standard=used_standard,
                )
                new_washer.save()
        print("Bolts 8.8 and 10.9 were added ")
