from django.test import TestCase

from distance_checker.calculation import CreatingCorner
from EngSolver.test import evaluate


class CreatingCornerTestCase(TestCase):
    def test_should_return_top_and_bottom_value_for_equal_parts(self):
        tested = CreatingCorner()
        tested_value = tested.creating_lines(
            girder_angle=15.0,
            girder_height=400,
            t_flange_girder=20,
            column_width=400,
            t_flange_column=20,
            t_plate_connection=30,
            total_length_bolt=92.5,
            space_for_screw=40,
        )
        tested_value_bottom, tested_value_top = tested_value[1]
        expected = 128
        delta = evaluate(expected)
        self.assertAlmostEqual(tested_value_bottom, expected, delta=delta)
        self.assertAlmostEqual(tested_value_top, expected, delta=delta)

    def test_should_return_top_and_bottom_value_for_not_equal_parts(self):
        tested = CreatingCorner()
        tested_value = tested.creating_lines(
            girder_angle=14.5,
            girder_height=400,
            t_flange_girder=20,
            column_width=700,
            t_flange_column=20,
            t_plate_connection=20,
            total_length_bolt=92.5,
            space_for_screw=40,
        )
        tested_value_bottom, tested_value_top = tested_value[1]
        expected_top = 218
        expected_bottom = 133
        delta_top = evaluate(expected_top)
        delta_bottom = evaluate(expected_bottom)
        self.assertAlmostEqual(tested_value_bottom, expected_bottom, delta=delta_bottom)
        self.assertAlmostEqual(tested_value_top, expected_top, delta=delta_top)
