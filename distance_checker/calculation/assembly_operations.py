from typing import Union

from ..models import Bolt, Nut, Washer


class FindingBolt:
    BOLTS_STANDARDS = {
        "8_8": ["EN-ISO-4032", "EN-ISO-4014", "EN-ISO-7089"],
        "10_9": ["14399-4D", "14399-4", "14399-5", "14399-6"],
    }

    THREAD_END = {
        4: 2.5,
        7: 4,
        12: 5,
        16: 6,
        22: 7,
        27: 8,
        33: 10,
    }

    def finding_thread_end(self, bolt_diameter: int) -> Union[int, float]:
        thread_end = self.THREAD_END
        for diameter, thread in thread_end.items():
            if bolt_diameter < diameter:
                return thread
        return 10

    def searching_assembly_parts(
        self, bolt_grade: str, bolt_diameter: int, thickness_plate: float
    ) -> [Bolt, Washer]:
        thread_end = self.finding_thread_end(bolt_diameter)

        chosen_standard = self.BOLTS_STANDARDS.get(bolt_grade)

        searched_bolt = Bolt.objects.filter(
            diameter=bolt_diameter, standard__title__in=chosen_standard
        ).order_by("length")

        searched_nut = Nut.objects.filter(
            diameter=bolt_diameter, standard__title__in=chosen_standard
        ).first()

        searched_washer = Washer.objects.filter(
            diameter=bolt_diameter, standard__title__in=chosen_standard
        ).first()

        thickness_nut = searched_nut.thickness_nut
        thickness_washer = searched_washer.thickness_washer

        basic_clamping_length = (
            2 * thickness_washer + thickness_nut + 2 * thickness_plate + thread_end
        )

        if bolt_grade == "10_9":
            for bolt in searched_bolt:
                shaft_length = bolt.length - bolt.thread_length - thread_end
                if shaft_length >= 2 * thickness_plate + thickness_washer - 3:
                    return bolt, searched_washer

            return None

        else:
            searched_bolt = searched_bolt.filter(
                length__gt=basic_clamping_length
            ).first()
        return searched_bolt, searched_washer


class ThicknessPartsAssembly:
    @staticmethod
    def space_for_screw(used_bolt: Bolt, thickness_plate: int) -> int:
        space = used_bolt.length - 2 * thickness_plate

        return space

    @staticmethod
    def total_length_bolt(used_bolt: Bolt) -> float:
        total_length_bolt = used_bolt.length + used_bolt.thickness_bolt_head
        return total_length_bolt

    @staticmethod
    def adding_w_bolt_head(used_bolt: Bolt, distance: float) -> float:
        distance_with_head = used_bolt.thickness_bolt_head / 2 + distance
        return distance_with_head
