from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

from bars_calculation.models import CalculationRhs, ProfileRhs
from distance_checker.models import Corner, Ridge


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser', password='testpass'
        )  # nosec B106

        self.user_empty = User.objects.create(
            username='testuser1', password='testpass1'
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

        self.corner_2 = Corner.objects.create(
            case="test",
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

        self.ridge = Ridge.objects.create(
            case="test",
            left_girder_angle=30,
            right_girder_angle=30,
            girder_height=500,
            left_t_flange_girder=20,
            right_t_flange_girder=20,
            t_plate_connection=20,
            bolt_grade="8_8",
            bolt_diameter=20,
            author=self.user,
            distance_left=100,
            distance_right=100,
        )

        self.profile = ProfileRhs.objects.create(
            name='test',
            H=1,
            B=1,
            T=1,
            G=1,
            surf=1,
            r0=1,
            r1=1,
            A=1,
            Ix=1,
            Iy=1,
            Iz=1,
            Wply=1,
            Wplz=1,
        )

        self.calculation = CalculationRhs.objects.create(
            case="test",
            type_profile='CF',
            country='Denmark',
            steel='S235',
            axial_force=10,
            eccentricity_y=10,
            eccentricity_z=10,
            bending_moment_y=10,
            bending_moment_z=10,
            shear_force_y=10,
            shear_force_z=10,
            length_profile=10,
            buckling_factor=10,
            limit_deformation=10,
            profile=self.profile,
            author=self.user,
            cross_section_class=1,
        )


# @tag('x')
class CornerDeleteViewTestCase(BaseTestCase):
    # self.corner = CornerFactory.create()
    # dopytac o post i get, czy jest rożnica pomiędzy testowanie tylko dostępu nie samej akcji

    tested_view = 'corner_delete'

    def test_delete_corner_return_302_when_user_not_logged_in(self):
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_delete_corner_return_200_when_user_not_logged_in_with_follow(self):
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk}), follow=True
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_delete_corner_return_302_when_correct_deleted_object(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Corner.objects.count(), 1)
        self.assertRedirects(response, reverse('dashboard'))

    @tag("x")
    def test_delete_corner_render_confirm_template(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk})
        )
        self.assertTemplateUsed(response, 'dashboard/delete_confirm.html')

    def test_delete_corner_return_302_when_wrong_user_logged_in(self):
        self.client.force_login(self.user_empty)
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)


class CalculationsViewViewTestCase(BaseTestCase):
    def test_calculation_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_calculation_view_return_200_when_user_not_logged_in_with_follow(self):
        response = self.client.get(reverse('dashboard'), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    @tag('x')
    def test_view_url_exists_at_desired_location_when_logged_with_qty_elements(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('qty_corners', response.context)
        qty_corners_value = response.context['qty_corners']
        qty_ridge_value = response.context['qty_ridges']
        qty_bars_value = response.context['qty_bars']
        self.assertEqual(qty_corners_value, 2)
        self.assertEqual(qty_ridge_value, 1)
        self.assertEqual(qty_bars_value, 1)

    def test_view_url_exists_at_desired_location_when_logged_without_any_qty_elements(
        self,
    ):
        self.client.force_login(self.user_empty)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('qty_corners', response.context)
        qty_corners_value = response.context['qty_corners']
        qty_ridge_value = response.context['qty_ridges']
        qty_bars_value = response.context['qty_bars']
        self.assertEqual(qty_corners_value, 0)
        self.assertEqual(qty_ridge_value, 0)
        self.assertEqual(qty_bars_value, 0)


class CornerCalculationViewTestCase(BaseTestCase):
    tested_url = reverse('corner_view')

    def test_calculation_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(self.tested_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_calculation_view_return_200_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_calculation_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertTemplateUsed(response, 'dashboard/corner.html')

    # dopytac o context i context data.

    def test_calculation_view_return_qty_corners_by_author(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertEqual(len(response.context['Corners']), 2)

    def test_calculation_view_return_qty_corners_by_author_without_any_qty_elements(
        self,
    ):
        self.client.force_login(self.user_empty)
        response = self.client.get(self.tested_url)
        self.assertEqual(len(response.context['Corners']), 0)

    # # dopytać skad wyciagnac albo jak sprawdzic auto
    # @tag('x')
    # def test_calculation_view_filter_context_by_search_bar(self):
    #     self.client.force_login(self.user)
    #     form_data = {"case": "case1"}
    #     response = self.client.get(reverse('corner_view'), form_data)
    #     expected_queryset = Corner.objects.filter(author=self.user, case='case1').order_by("-created_date")
    #     self.assertQuerysetEqual(response.context['Corners'], expected_queryset, transform=repr)
