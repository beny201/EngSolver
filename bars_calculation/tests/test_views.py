from http import HTTPStatus
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

from ..models import CalculationRhs, ProfileRhs
from .factories import ProfileRhsUseFactory


@tag('x')
class CalculationRhsViewTestCase(TestCase):
    @staticmethod
    def evaluate(value):
        ev_1 = value * 0.99
        ev_2 = value * 1.01

        return ev_2 - ev_1

    def setUp(self):
        self.user = User.objects.create(
            username='testuser', password='testpass'
        )  # nosec B106

        self.profile = ProfileRhs.objects.create(
            name='test2',
            H=120,
            B=100,
            T=4,
            G=4,
            surf=4,
            r0=4,
            r1=4,
            A=16.55 * (10**2),
            Ix=348 * (10**4),
            Iy=348 * (10**4),
            Iz=263 * (10**4),
            Wply=69.05 * (10**3),
            Wplz=60.98 * (10**3),
        )

        self.test_form_positive = {
            'case': 3000,
            'type_profile': "CF",
            'country': "Sweden",
            'steel': "S355",
            'axial_force': 50,
            'eccentricity_y': 0,
            'eccentricity_z': 0,
            'bending_moment_y': 1,
            'bending_moment_z': 2,
            'shear_force_y': 10,
            'shear_force_z': 20,
            'buckling_factor': 1,
            'length_profile': 5,
            'limit_deformation': 200,
            'profile': self.profile,
        }

        self.test_form_negative = self.test_form_positive.copy()
        self.test_form_negative['axial_force'] = -50

    def test_calculation_view_return_200(self):
        response = self.client.get(reverse('calculation_bar'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'bars_calculation/bar.html')
        self.assertEqual(response.context['title'], "Bars calculation")
        self.assertEqual(response.context['connection_type'], "Design RHS, SHS checker")

    def test_calculation_form_is_valid_and_axial_is_positive(self):
        response = self.client.post(
            reverse('calculation_bar'), data=self.test_form_positive
        )

        self.assertIn('utilization_shear', response.context)
        expected = 0.108
        delta = self.evaluate(expected)
        utilization_shear = response.context['utilization_shear']
        self.assertAlmostEqual(utilization_shear, expected, delta=delta)

        self.assertIn('utilization_tension', response.context)
        expected = 0.108
        delta = self.evaluate(expected)
        utilization_tension = response.context['utilization_tension']
        self.assertAlmostEqual(utilization_tension, expected, delta=delta)

        self.assertIn('utilization_deformation', response.context)
        expected = 0.45
        delta = self.evaluate(expected)
        utilization_deformation = response.context['utilization_deformation']
        self.assertAlmostEqual(utilization_deformation, expected, delta=delta)

        self.assertIn('list_of_lightest_profiles_tension', response.context)

        self.assertNotIn('utilization_compression', response.context)
        self.assertNotIn('list_of_lightest_profiles_compression', response.context)
        self.assertTemplateUsed(response, 'bars_calculation/bar.html')

    def test_calculation_form_is_valid_and_axial_is_negative(self):
        response = self.client.post(
            reverse('calculation_bar'), data=self.test_form_negative
        )

        self.assertIn('utilization_shear', response.context)
        expected = 0.108
        delta = self.evaluate(expected)
        utilization_shear = response.context['utilization_shear']
        self.assertAlmostEqual(utilization_shear, expected, delta=delta)

        self.assertIn('utilization_compression', response.context)
        expected = 0.461
        delta = self.evaluate(expected)
        utilization_compression = response.context['utilization_compression']
        self.assertAlmostEqual(utilization_compression, expected, delta=delta)

        self.assertIn('utilization_deformation', response.context)
        expected = 0.45
        delta = self.evaluate(expected)
        utilization_deformation = response.context['utilization_deformation']
        self.assertAlmostEqual(utilization_deformation, expected, delta=delta)

        self.assertIn('list_of_lightest_profiles_compression', response.context)

        self.assertNotIn('utilization_tension', response.context)
        self.assertNotIn('list_of_lightest_profiles_tension', response.context)
        self.assertTemplateUsed(response, 'bars_calculation/bar.html')

    def test_should_save_calculation_to_db(self):
        self.client.force_login(self.user)
        save_action = {'save_db': 'save_to_db'}
        self.test_form_negative.update(save_action)
        response = self.client.post(
            reverse('calculation_bar'), data=self.test_form_negative
        )
        self.assertEqual(CalculationRhs.objects.count(), 1)
        self.assertContains(response, "Connection was saved to Database !")

    @patch('bars_calculation.views.CrossSectionClass')
    def test_should_check_if_there_is_warning_when_4_class_reached(
        self, mock_cross_section_class
    ):
        mock_instance = MagicMock()
        mock_instance.check_class.return_value = 4
        mock_cross_section_class.return_value = mock_instance
        response = self.client.post(
            reverse('calculation_bar'), data=self.test_form_negative
        )
        self.assertContains(
            response, "Cross section class 4 (Calculation will be made as for 3) !"
        )

    @patch('bars_calculation.views.CalculationRHS')
    def test_should_check_if_there_is_warning_when_capacity_is_exceeded(
        self, mock_total_deformation
    ):
        mock_instance = MagicMock()
        mock_instance.check_deformation.return_value = 2
        mock_total_deformation.return_value = mock_instance
        response = self.client.post(
            reverse('calculation_bar'), data=self.test_form_negative
        )
        self.assertContains(response, "Capacity exceeded !")

    def test_should_check_if_4_compressed_profiles_are_shown(self):
        ProfileRhsUseFactory.create_batch(10)
        response = self.client.post(
            reverse('calculation_bar'), data=self.test_form_negative
        )
        self.assertEqual(
            len(response.context['list_of_lightest_profiles_compression']), 4
        )

    def test_should_check_if_4_tensioned_profiles_are_shown(self):
        ProfileRhsUseFactory.create_batch(10)
        response = self.client.post(
            reverse('calculation_bar'), data=self.test_form_positive
        )
        self.assertEqual(len(response.context['list_of_lightest_profiles_tension']), 4)
