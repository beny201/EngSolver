from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, ListView

from distance_checker.models import Corner

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


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'users/profile.html'
    model = Corner
    context_object_name = "Corners"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(author=user).order_by("-created_date")
        return queryset


class ConnectionView(LoginRequiredMixin, DetailView):
    model = Corner
    context_object_name = "corner"
    template_name = 'users/profile_detail.html'


class DeleteConnectionView(LoginRequiredMixin, DeleteView):
    model = Corner
    context_object_name = "corner"
    template_name = 'users/delete_confirm.html'
    success_url = reverse_lazy('profile')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('change_password')

    def form_valid(self, form):
        username = self.request.user
        messages.success(self.request, f"Hello {username}, password was changed !")
        return super().form_valid(form)
