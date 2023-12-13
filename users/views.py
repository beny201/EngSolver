from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import UserRegisterForm


class UserRegistrationView(FormView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Welcome {username}, you have been logged !")
        user = form.save()
        login(self.request, user)
        return redirect(reverse("register"))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profiles')

    def form_valid(self, form):
        username = self.request.user
        messages.success(self.request, f"Hello {username}, password was changed !")
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
