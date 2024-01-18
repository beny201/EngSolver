from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import CustomPasswordChangeView, ProfileView, UserRegistrationView, activate

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(
        'logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'
    ),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]
