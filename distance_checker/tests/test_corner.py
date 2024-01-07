from django.test import TestCase, tag

from distance_checker.calculation import CreatingCorner


class CreatingCornerTestCase(TestCase):
    @staticmethod
    def evaluate(value):
        ev_1 = value * 0.99
        ev_2 = value * 1.01

        return ev_2 - ev_1

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
        delta = self.evaluate(expected)
        self.assertAlmostEqual(tested_value_bottom, expected, delta=delta)
        self.assertAlmostEqual(tested_value_top, expected, delta=delta)

    @tag("x")
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
        print(tested_value)
        expected_top = 218
        expected_bottom = 133
        delta_top = self.evaluate(expected_top)
        delta_bottom = self.evaluate(expected_bottom)
        self.assertAlmostEqual(tested_value_bottom, expected_bottom, delta=delta_bottom)
        self.assertAlmostEqual(tested_value_top, expected_top, delta=delta_top)
