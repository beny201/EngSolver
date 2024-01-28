from http import HTTPStatus

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser', password='testpass', email='test1@gmail.com'
        )  # nosec B106


class ProfileViewTestCase(BaseTestCase):
    def test_profile_view_return_302_when_user_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('login', response.url)

    def test_profile_view_return_200_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')


class CustomPasswordResetViewTestCase(BaseTestCase):
    def test_password_reset_view(self):
        response = self.client.post(
            reverse('reset_password'), {'email': self.user.email}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('token', response.context)
        self.assertIn('login', response.url)

    def test_should_return_used_template_for_password_reset_view(self):
        response = self.client.get(reverse('reset_password'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/change_password.html')


class CustomPasswordConfirmResetViewTestCase(BaseTestCase):
    def test_password_reset_confirm_view(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self.user)
        url = reverse(
            'password_reset_confirm', kwargs={'uidb64': uid, 'token': 'set-password'}
        )
        self.client.get(url)
        session = self.client.session
        session['_password_reset_token'] = token
        session.save()
        valid_data = {
            "new_password1": ")44Y5y5L5ntjQa&",
            "new_password2": ")44Y5y5L5ntjQa&",
        }
        response = self.client.post(url, valid_data)
        self.assertRedirects(response, reverse('profile'))


class UserRegistrationViewTestCase(TestCase):
    def test_user_registration_view_200_(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_should_check_if_email_is_sent(self):
        data = {
            'username': 'username',
            'email': ' test@wp.pl',
            'password1': ")44Y5y5L5ntjQa&",
            'password2': ")44Y5y5L5ntjQa&",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Activate your user account.")
