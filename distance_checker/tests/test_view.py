from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class BasicViewTestCase(TestCase):
    def test_basic_view_return(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'distance_checker/index.html')


# class DistanceCornerViewViewTestCase(TestCase):
#     @staticmethod
#     def evaluate(value):
#         ev_1 = value * 0.99
#         ev_2 = value * 1.01
#
#         return ev_2 - ev_1
#
#     def setUp(self):
#         self.user = User.objects.create(
#             username='testuser', password='testpass'
#         )  # nosec B106
#
#         self.profile = ProfileRhs.objects.create(
#             name='test2',
#             H=120,
#             B=100,
#             T=4,
#             G=4,
#             surf=4,
#             r0=4,
#             r1=4,
#             A=16.55 * (10**2),
#             Ix=348 * (10**4),
#             Iy=348 * (10**4),
#             Iz=263 * (10**4),
#             Wply=69.05 * (10**3),
#             Wplz=60.98 * (10**3),
#         )
#
#         self.test_form_positive = {
#             'case': 3000,
#             'type_profile': "CF",
#             'country': "Sweden",
#             'steel': "S355",
#             'axial_force': 50,
#             'eccentricity_y': 0,
#             'eccentricity_z': 0,
#             'bending_moment_y': 1,
#             'bending_moment_z': 2,
#             'shear_force_y': 10,
#             'shear_force_z': 20,
#             'buckling_factor': 1,
#             'length_profile': 5,
#             'limit_deformation': 200,
#             'profile': self.profile,
#         }
#
#         self.test_form_negative = self.test_form_positive.copy()
#         self.test_form_negative['axial_force'] = -50
#
#     def test_calculation_view_return_200(self):
#         response = self.client.get(reverse('calculation_bar'))
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertTemplateUsed(response, 'bars_calculation/bar.html')
#         self.assertEqual(response.context['title'], "Bars calculation")
#         self.assertEqual(response.context['connection_type'], "Design RHS, SHS checker")
