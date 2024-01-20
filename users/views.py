from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, TemplateView

from .forms import UserRegisterForm
from .tokens import account_activation_token


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except ObjectDoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect('register')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('login')


class UserRegistrationView(FormView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def activateEmail(self, user, to_email):
        mail_subject = "Activate your user account."
        message = render_to_string(
            "users/activate_account.html",
            {
                'user': user.username,
                'domain': get_current_site(self.request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                "protocol": 'https' if self.request.is_secure() else 'http',
            },
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            messages.success(
                self.request,
                f"Dear {user}, please go to you email {to_email} inbox and click on received activation \n"
                f"link to confirm and complete the registration. \n"
                f"Check your spam folder.",
            )

        else:
            messages.error(
                self.request,
                f"Problem sending email to {to_email}, check if you typed it correctly",
            )

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.activateEmail(user, form.cleaned_data.get('email'))
        return redirect(reverse("register"))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        username = self.request.user
        messages.success(self.request, f"Hello {username}, password was changed !")
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request,
            "Password reset link was sent to e-mail if an account exists.",
        )
        return super().form_valid(form)


class CustomPasswordConfirmResetView(PasswordResetConfirmView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile')
    post_reset_login = True

    def form_valid(self, form):
        messages.success(self.request, 'Password was changed')
        login(self.request, self.user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
