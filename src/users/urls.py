from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    ConnectionView,
    CustomPasswordChangeView,
    DeleteConnectionView,
    ProfileView,
    UserRegistrationView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(
        'logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'
    ),
    path('profiles/', ProfileView.as_view(), name='profiles'),
    path('profiles/<int:pk>', ConnectionView.as_view(), name='connection_detail'),
    path('change/', CustomPasswordChangeView.as_view(), name='change_password'),
    path(
        'profiles/<int:pk>/delete',
        DeleteConnectionView.as_view(),
        name='connection_delete',
    ),  # profiles/<int:pk>/delete # users/<int:pk>/profiles/<int:profile>
]
