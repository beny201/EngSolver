from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView

# from src.distance_checker.models import WasherStandard
from .forms import UserRegisterForm


def register(request):  # TODO CLASS BASED VIEW.
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Welcome {username}, you have been " f"logged  !"
            )
            user = form.save()
            login(request, user)
            return redirect(reverse("register"))

    else:
        return render(
            request,
            "user/register.html",
            {"form": UserRegisterForm, 'title': "Register"},
        )


class ViewAllData(CreateView):
    model = User


class ChangePassword(PasswordChangeView):
    template_name = 'user/change_password.html'
