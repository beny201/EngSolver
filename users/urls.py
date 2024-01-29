from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    ContactView,
    CustomPasswordChangeView,
    CustomPasswordConfirmResetView,
    CustomPasswordResetView,
    ProfileView,
    UserRegistrationView,
    activate,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(
        'logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'
    ),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('reset/', CustomPasswordResetView.as_view(), name='reset_password'),
    path(
        'reset/<uidb64>/<token>',
        CustomPasswordConfirmResetView.as_view(),
        name='password_reset_confirm',
    ),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('contact', ContactView.as_view(), name='contact'),
]
