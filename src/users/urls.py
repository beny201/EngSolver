from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import ChangePassword, RegisterUser, ViewProfile

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(
        'logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'
    ),
    path('profile/', ViewProfile.as_view(), name='profile'),
    path('change/', ChangePassword.as_view(), name='change_password'),
]
