from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

from distance_checker.models import Corner


class CornerDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser', password='testpass'
        )  # nosec B106

        self.corner = Corner.objects.create(
            case="case1",
            girder_angle=30,
            girder_height=500,
            t_flange_girder=20,
            column_width=500,
            t_flange_column=20,
            t_plate_connection=20,
            bolt_grade="8_8",
            bolt_diameter=20,
            author=self.user,
            distance_top=100,
            distance_bottom=100,
        )

        # self.corner = CornerFactory.create()

    def test_delete_corner_return_403_when_user_not_logged_in(self):
        response = self.client.get(
            reverse('corner_delete', kwargs={'pk': self.corner.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_delete_corner_return_403_when_user_not_logged_in_with_follow(self):
        response = self.client.get(
            reverse('corner_delete', kwargs={'pk': self.corner.pk}), follow=True
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    @tag('x')
    def test_delete_corner_return_200_when_correct_deleted_object(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('corner_delete', kwargs={'pk': self.corner.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Corner.objects.count(), 0)
