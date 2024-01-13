from django.test import TestCase

from distance_checker.calculation import CreatingRidge
from EngSolver.test import evaluate


class CreatingRidgeTestCase(TestCase):
    def test_should_return_left_and_right_value_for_equal_parts(self):
        tested = CreatingRidge()
        tested_value = tested.creating_lines(
            left_girder_angle=14.5,
            right_girder_angle=14.5,
            girder_height=400,
            left_t_flange_girder=20,
            right_t_flange_girder=20,
            t_plate_connection=20,
            total_length_bolt=92.5,
            space_for_screw=40,
        )
        tested_value_left, tested_value_right = tested_value[1]
        expected = 50
        delta = evaluate(expected)
        self.assertAlmostEqual(tested_value_left, expected, delta=delta)
        self.assertAlmostEqual(tested_value_right, expected, delta=delta)

    def test_should_return_left_and_right_value_for_not_equal_parts(self):
        tested = CreatingRidge()
        tested_value = tested.creating_lines(
            left_girder_angle=14.5,
            right_girder_angle=20,
            girder_height=400,
            left_t_flange_girder=20,
            right_t_flange_girder=20,
            t_plate_connection=20,
            total_length_bolt=92.5,
            space_for_screw=40,
        )
        tested_value_left, tested_value_right = tested_value[1]
        expected_left = 50
        expected_right = 62
        delta_left = evaluate(expected_left)
        delta_right = evaluate(expected_right)
        self.assertAlmostEqual(tested_value_left, expected_left, delta=delta_left)
        self.assertAlmostEqual(tested_value_right, expected_right, delta=delta_right)
