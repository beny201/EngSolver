from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from EngSolver.test import evaluate

from ..models import (
    Bolt,
    BoltStandard,
    Corner,
    Nut,
    NutStandard,
    Ridge,
    Washer,
    WasherStandard,
)


class BasicViewTestCase(TestCase):
    def test_basic_view_return(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'distance_checker/index.html')


class BaseTestCase(TestCase):
    def setUp(self):
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

        self.bolt_10_9_2 = Bolt.objects.create(
            name="M20*120",
            thickness_bolt_head=12.5,
            width_bolt_head=30.0,
            length=120,
            diameter=20,
            thread_length=46,
            standard=self.bolt_standard_10_9,
        )

        self.test_corner = {
            'case': 2000,
            'girder_angle': 15.0,
            'girder_height': 400,
            't_flange_girder': 20,
            'column_width': 400,
            't_flange_column': 20,
            't_plate_connection': 30,
            'bolt_grade': '8_8',
            'bolt_diameter': 20,
        }

        self.test_corner_2 = {
            'case': 3000,
            'girder_angle': 14.5,
            'girder_height': 400,
            't_flange_girder': 20,
            'column_width': 700,
            't_flange_column': 20,
            't_plate_connection': 30,
            'bolt_grade': '8_8',
            'bolt_diameter': 20,
        }

        self.test_ridge = {
            'case': 2000,
            'left_girder_angle': 14.5,
            'right_girder_angle': 14.5,
            'girder_height': 400,
            'left_t_flange_girder': 20,
            'right_t_flange_girder': 20,
            't_plate_connection': 20,
            'bolt_grade': '8_8',
            'bolt_diameter': 20,
        }

        self.test_ridge_2 = {
            'case': 2000,
            'left_girder_angle': 14.5,
            'right_girder_angle': 20,
            'girder_height': 400,
            'left_t_flange_girder': 20,
            'right_t_flange_girder': 20,
            't_plate_connection': 20,
            'bolt_grade': '8_8',
            'bolt_diameter': 20,
        }

        self.url_corner = reverse('corner_distance')
        self.url_ridge = reverse('ridge_distance')


class DistanceCornerViewViewTestCase(BaseTestCase):
    def test_calculation_view_return_200_for_corner(self):
        response = self.client.get(self.url_corner)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'distance_checker/frame_connection.html')
        self.assertEqual(response.context['title'], "Corner distance")
        self.assertEqual(response.context['connection_type'], "Corner checker")

    def test_form_should_return_top_and_bottom_value_for_equal_parts_for_corner(self):
        response = self.client.post(self.url_corner, data=self.test_corner)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('image_data', response.context)
        self.assertIn('distance_from_bottom', response.context)
        self.assertIn('distance_from_top', response.context)

        tested_value_bottom = response.context['distance_from_bottom']
        tested_value_top = response.context['distance_from_top']
        expected = 152
        delta = evaluate(expected)
        self.assertAlmostEqual(tested_value_bottom, expected, delta=delta)
        self.assertAlmostEqual(tested_value_top, expected, delta=delta)

    def test_form_should_return_top_and_bottom_value_for_corner(self):
        response = self.client.post(self.url_corner, data=self.test_corner_2)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('image_data', response.context)
        self.assertIn('distance_from_bottom', response.context)
        self.assertIn('distance_from_top', response.context)

        tested_value_bottom = response.context['distance_from_bottom']
        tested_value_top = response.context['distance_from_top']
        expected_top = 273
        expected_bottom = 156
        delta_top = evaluate(expected_top)
        delta_bottom = evaluate(expected_bottom)
        self.assertAlmostEqual(tested_value_bottom, expected_bottom, delta=delta_bottom)
        self.assertAlmostEqual(tested_value_top, expected_top, delta=delta_top)

    def test_should_check_if_not_logged_can_save_for_corner(self):
        save_action = {'save_db': 'save_to_db'}
        self.test_corner_2.update(save_action)
        self.client.post(self.url_corner, data=self.test_corner_2)
        self.assertEqual(Corner.objects.count(), 0)

    def test_should_save_calculation_to_db_for_corner(self):
        self.client.force_login(self.user)
        save_action = {'save_db': 'save_to_db'}
        self.test_corner_2.update(save_action)
        response = self.client.post(self.url_corner, data=self.test_corner_2)
        self.assertEqual(Corner.objects.count(), 1)
        self.assertContains(response, "Connection was saved to Database !")

    def test_exception_handling(self):
        test_corner_3 = {
            'case': 3000,
            'girder_angle': 2.5,
            'girder_height': 100,
            't_flange_girder': 20,
            'column_width': 700,
            't_flange_column': 20,
            't_plate_connection': 30,
            'bolt_grade': '8_8',
            'bolt_diameter': 20,
        }
        response = self.client.post(self.url_corner, data=test_corner_3)
        self.assertContains(
            response,
            "Something went wrong, please check once more geometry of connection",
        )


class DistanceRidgeViewViewTestCase(BaseTestCase):
    def test_calculation_view_return_200_for_corner(self):
        response = self.client.get(self.url_ridge)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'distance_checker/frame_connection.html')
        self.assertEqual(response.context['title'], "Ridge distance")
        self.assertEqual(response.context['connection_type'], "Ridge checker")

    def test_form_should_return_top_and_bottom_value_for_equal_parts_for_corner(self):
        response = self.client.post(self.url_ridge, data=self.test_ridge)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('image_data', response.context)
        self.assertIn('distance_from_left', response.context)
        self.assertIn('distance_from_right', response.context)

        tested_value_bottom = response.context['distance_from_left']
        tested_value_top = response.context['distance_from_right']
        expected = 61
        delta = evaluate(expected)
        self.assertAlmostEqual(tested_value_bottom, expected, delta=delta)
        self.assertAlmostEqual(tested_value_top, expected, delta=delta)

    def test_form_should_return_top_and_bottom_value_for_corner(self):
        response = self.client.post(self.url_ridge, data=self.test_ridge_2)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('image_data', response.context)
        self.assertIn('distance_from_left', response.context)
        self.assertIn('distance_from_right', response.context)

        tested_value_left = response.context['distance_from_left']
        tested_value_right = response.context['distance_from_right']
        expected_left = 61
        expected_right = 76
        delta_left = evaluate(expected_left)
        delta_right = evaluate(expected_right)
        self.assertAlmostEqual(tested_value_left, expected_left, delta=delta_left)
        self.assertAlmostEqual(tested_value_right, expected_right, delta=delta_right)

    def test_should_check_if_not_logged_can_save_for_corner(self):
        save_action = {'save_db': 'save_to_db'}
        self.test_corner_2.update(save_action)
        self.client.post(self.url_ridge, data=self.test_ridge_2)
        self.assertEqual(Ridge.objects.count(), 0)

    def test_should_save_calculation_to_db_for_corner(self):
        self.client.force_login(self.user)
        save_action = {'save_db': 'save_to_db'}
        self.test_ridge_2.update(save_action)
        response = self.client.post(self.url_ridge, data=self.test_ridge_2)
        self.assertEqual(Ridge.objects.count(), 1)
        self.assertContains(response, "Connection was saved to Database !")

    def test_exception_handling(self):
        test_ridge_3 = {
            'case': 2000,
            'left_girder_angle': 5,
            'right_girder_angle': 14.5,
            'girder_height': 2000,
            'left_t_flange_girder': 20,
            'right_t_flange_girder': 20,
            't_plate_connection': 20,
            'bolt_grade': '8_8',
            'bolt_diameter': 20,
        }
        response = self.client.post(self.url_ridge, data=test_ridge_3)
        self.assertContains(
            response,
            "Something went wrong, please check once more geometry of connection",
        )
