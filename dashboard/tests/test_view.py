from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

from bars_calculation.models import CalculationRhs
from distance_checker.models import Corner, Ridge

from .factories import (
    CalculationRhsUseFactory,
    CornerUseFactory,
    ProfileRhsUseFactory,
    RidgeUseFactory,
)


@tag("x")
class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser', password='testpass'
        )  # nosec B106

        self.user_empty = User.objects.create(
            username='testuser1', password='testpass1'
        )  # nosec B106

        self.corner = CornerUseFactory(author=self.user)
        self.corner_1 = CornerUseFactory(author=self.user, case="test1")
        self.ridge = RidgeUseFactory(author=self.user)
        self.profile = ProfileRhsUseFactory()
        self.calculation = CalculationRhsUseFactory(
            profile=self.profile, author=self.user
        )


class CalculationsViewViewTestCase(BaseTestCase):
    def test_calculation_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_calculation_view_return_200_when_user_not_logged_in_with_follow(self):
        response = self.client.get(reverse('dashboard'), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

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

    def test_calculation_corner_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(self.tested_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_calculation_corner_view_return_200_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_calculation_corner_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertTemplateUsed(response, 'dashboard/corner.html')

    def test_calculation_corner_view_return_qty_corners_by_author(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertEqual(len(response.context['Corners']), 2)

    def test_calculation_corner_view_return_qty_corners_by_author_without_any_qty_elements(
        self,
    ):
        self.client.force_login(self.user_empty)
        response = self.client.get(self.tested_url)
        self.assertEqual(len(response.context['Corners']), 0)

    def test_calculation_view_filter_context_by_search_bar(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('corner_view'), {'case': 'case1'})
        expected_queryset = Corner.objects.filter(
            author=self.user, case='case1'
        ).order_by("-created_date")
        self.assertQuerysetEqual(response.context['Corners'], expected_queryset)


class CornerDetailViewTestCase(BaseTestCase):
    tested_view = 'corner_detail'

    def test_detail_corner_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_detail_corner_view_return_200_when_user_not_logged_in_with_follow(self):
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_detail_corner_view_200_when_correct_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['object'], self.corner)
        self.assertTemplateUsed(response, 'dashboard/corner_detail.html')

    def test_detail_corner_view_302_when_incorrect_user_logged_in(self):
        self.client.force_login(self.user_empty)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.corner.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)


class CornerDeleteViewTestCase(BaseTestCase):
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


class RidgeCalculationViewTestCase(BaseTestCase):
    tested_url = reverse('ridge_view')

    def test_calculation_ridge_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(self.tested_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_calculation_ridge_view_return_200_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_calculation_ridge_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertTemplateUsed(response, 'dashboard/ridge.html')

    def test_calculation_ridge_view_return_qty_corners_by_author(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertEqual(len(response.context['Ridges']), 1)

    def test_calculation_ridge_view_return_qty_corners_by_author_without_any_qty_elements(
        self,
    ):
        self.client.force_login(self.user_empty)
        response = self.client.get(self.tested_url)
        self.assertEqual(len(response.context['Ridges']), 0)

    def test_calculation_ridge_view_filter_context_by_search_bar(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('ridge_view'), {'case': 'case1'})
        expected_queryset = Ridge.objects.filter(
            author=self.user, case='case1'
        ).order_by("-created_date")
        self.assertQuerysetEqual(response.context['Ridges'], expected_queryset)


class RidgeDetailViewTestCase(BaseTestCase):
    tested_view = 'ridge_detail'

    def test_detail_ridge_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_detail_ridge_view_return_200_when_user_not_logged_in_with_follow(self):
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_detail_ridge_view_200_when_correct_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['object'], self.ridge)
        self.assertTemplateUsed(response, 'dashboard/ridge_detail.html')

    def test_detail_ridge_view_302_when_incorrect_user_logged_in(self):
        self.client.force_login(self.user_empty)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)


class RidgeDeleteViewTestCase(BaseTestCase):
    tested_view = 'ridge_delete'

    def test_delete_ridge_return_302_when_user_not_logged_in(self):
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_delete_ridge_return_200_when_user_not_logged_in_with_follow(self):
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_delete_ridge_return_302_when_correct_deleted_object(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Ridge.objects.count(), 0)
        self.assertRedirects(response, reverse('dashboard'))

    def test_delete_ridge_render_confirm_template(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk})
        )
        self.assertTemplateUsed(response, 'dashboard/delete_confirm.html')

    def test_delete_ridge_return_302_when_wrong_user_logged_in(self):
        self.client.force_login(self.user_empty)
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.ridge.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)


class BarCalculationViewTestCase(BaseTestCase):
    tested_url = reverse('bars_view')

    def test_calculation_bar_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(self.tested_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_calculation_bar_view_return_200_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_calculation_bar_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertTemplateUsed(response, 'dashboard/bar.html')

    def test_calculation_bar_view_return_qty_corners_by_author(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tested_url)
        self.assertEqual(len(response.context['calculation']), 1)

    def test_calculation_bar_view_return_qty_corners_by_author_without_any_qty_elements(
        self,
    ):
        self.client.force_login(self.user_empty)
        response = self.client.get(self.tested_url)
        self.assertEqual(len(response.context['calculation']), 0)

    def test_calculation_bar_view_filter_context_by_search_bar(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('bars_view'), {'case': 'case1'})
        expected_queryset = CalculationRhs.objects.filter(
            author=self.user, case='case1'
        ).order_by("-created_date")
        self.assertQuerysetEqual(response.context['calculation'], expected_queryset)


class BarDetailViewTestCase(BaseTestCase):
    tested_view = 'bar_detail'

    def test_detail_bar_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_detail_bar_view_return_200_when_user_not_logged_in_with_follow(self):
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_detail_bar_view_200_when_correct_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['object'], self.calculation)
        self.assertTemplateUsed(response, 'dashboard/bar_detail.html')

    def test_detail_bar_view_302_when_incorrect_user_logged_in(self):
        self.client.force_login(self.user_empty)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)


class BarDeleteViewTestCase(BaseTestCase):
    tested_view = 'bar_delete'

    def test_delete_bar_return_302_when_user_not_logged_in(self):
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_delete_bar_return_200_when_user_not_logged_in_with_follow(self):
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_delete_bar_return_302_when_correct_deleted_object(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(CalculationRhs.objects.count(), 0)
        self.assertRedirects(response, reverse('dashboard'))

    def test_delete_bar_render_confirm_template(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk})
        )
        self.assertTemplateUsed(response, 'dashboard/delete_confirm.html')

    def test_delete_bar_return_302_when_wrong_user_logged_in(self):
        self.client.force_login(self.user_empty)
        response = self.client.post(
            reverse(self.tested_view, kwargs={'pk': self.calculation.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)
