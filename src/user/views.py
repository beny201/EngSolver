from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from src.user.forms import UserRegisterForm
from django.contrib import messages


def register(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            messages.success(request, f"Welcome {username}, you have been "
                                      f"logged  !")
            user = form.save()
            login(request, user)
            return redirect(reverse("register"))

    else:
        return render(
            request, "user/register.html",
            {"form": UserRegisterForm, 'title': "Register"}
        )

