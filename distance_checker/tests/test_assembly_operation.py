from django.contrib.auth.models import User
from django.test import TestCase

from distance_checker.calculation.assembly_operations import (
    FindingBolt,
    ThicknessPartsAssembly,
)

from ..models import Bolt, BoltStandard, Nut, NutStandard, Washer, WasherStandard


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='testuser', password='testpass'
        )  # nosec B106

        self.bolt_standard_8_8 = BoltStandard.objects.create(title='EN-ISO-4014')
        self.bolt_standard_10_9 = BoltStandard.objects.create(title='14399-4')
        self.washer_standard_8_8 = WasherStandard.objects.create(title='EN-ISO-7089')
        self.washer_standard_10_9 = WasherStandard.objects.create(title='14399-5')
        self.nut_standard_8_8 = NutStandard.objects.create(
            title='EN-ISO-4032',
        )
        self.nut_standard_10_9 = NutStandard.objects.create(
            title='14399-4D',
        )
        self.washer_8_8 = Washer.objects.create(
            name="RONDELLA-20",
            thickness_washer=3,
            width_washer=37.0,
            diameter=20,
            standard=self.washer_standard_8_8,
        )
        self.nut_8_8 = Nut.objects.create(
            name="DADO-20",
            thickness_nut=18,
            width_nut=30.0,
            diameter=20,
            standard=self.nut_standard_8_8,
        )
        self.bolt_8_8_1 = Bolt.objects.create(
            name="M20*100",
            thickness_bolt_head=12.5,
            width_bolt_head=30.0,
            length=100,
            diameter=20,
            thread_length=46,
            standard=self.bolt_standard_8_8,
        )
        self.bolt_8_8_2 = Bolt.objects.create(
            name="M20*120",
            thickness_bolt_head=12.5,
            width_bolt_head=30.0,
            length=120,
            diameter=20,
            thread_length=46,
            standard=self.bolt_standard_8_8,
        )
        self.washer_10_9 = Washer.objects.create(
            name="RONDELLA-20",
            thickness_washer=3,
            width_washer=37.0,
            diameter=20,
            standard=self.washer_standard_10_9,
        )
        self.nut_10_9 = Nut.objects.create(
            name="DADO-20",
            thickness_nut=18,
            width_nut=30.0,
            diameter=20,
            standard=self.nut_standard_10_9,
        )
        self.bolt_10_9_1 = Bolt.objects.create(
            name="M20*100",
            thickness_bolt_head=12.5,
            width_bolt_head=30.0,
            length=100,
            diameter=20,
            thread_length=46,
            standard=self.bolt_standard_10_9,
        )

        self.bolt_10_9_2 = Bolt.objects.create(
            name="M20*120",
            thickness_bolt_head=12.5,
            width_bolt_head=30.0,
            length=120,
            diameter=20,
            thread_length=46,
            standard=self.bolt_standard_10_9,
        )


class FindingBoltTestCase(BaseTestCase):
    def test_should_return_thread_of_used_bolt(self):
        bolts_part = FindingBolt()
        self.assertEqual(bolts_part.finding_thread_end(20), 7)
        self.assertEqual(bolts_part.finding_thread_end(33), 10)

    def test_should_return_searched_bolts_parts_for_8_8(self):
        bolts_part = FindingBolt()
        bolt_grade = "8_8"
        bolt_diameter = 20
        thickness_plate = 30
        self.assertEqual(
            bolts_part.searching_assembly_parts(
                bolt_grade, bolt_diameter, thickness_plate
            ),
            (self.bolt_8_8_1, self.washer_8_8),
        )

    def test_should_return_searched_bolts_parts_for_10_9(self):
        bolts_part = FindingBolt()
        bolt_grade = "10_9"
        bolt_diameter = 20
        thickness_plate = 30
        self.assertEqual(
            bolts_part.searching_assembly_parts(
                bolt_grade, bolt_diameter, thickness_plate
            ),
            (self.bolt_10_9_2, self.washer_10_9),
        )


class ThicknessPartsAssemblyTestCase(BaseTestCase):
    def test_should_return_space_for_screw(self):
        parts = ThicknessPartsAssembly()
        thickness_plate = 30
        self.assertEqual(parts.space_for_screw(self.bolt_8_8_1, thickness_plate), 40)

    def test_should_return_total_length_bolt(self):
        parts = ThicknessPartsAssembly()
        self.assertEqual(
            parts.total_length_bolt(
                self.bolt_8_8_1,
            ),
            112.5,
        )

    def test_should_return_total_adding_w_bolt_head(self):
        parts = ThicknessPartsAssembly()
        self.assertEqual(parts.adding_w_bolt_head(self.bolt_8_8_1, 50), 56.25)
