from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, ListView

from .forms import UserRegisterForm


class RegisterUser(FormView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Welcome {username}, you have been logged !")
        user = form.save()
        login(self.request, user)
        return redirect(reverse("register"))


class ViewProfile(LoginRequiredMixin, ListView):
    template_name = 'users/profile.html'
    model = User
    login_url = 'login'


class ChangePassword(PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = 'change_password'

    def get_success_url(self):
        return reverse('change_password')

    def form_valid(self, form):
        username = self.request.user
        print(username)
        messages.success(self.request, f"Hello {username}, password was changed !")
        return super().form_valid(form)
