"""
URL configuration for EngSolver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('distance_checker/', include("distance_checker.urls")),
    path('', include("distance_checker.urls")),
    path('register/', include("users.urls")),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='user/login.html'),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='user/logout.html'),
        name='logout',
    ),
    path(
        'profile/',
        user_views.ViewAllData.as_view(template_name='user/profile.html'),
        name='profile',
    ),
    path('change/', user_views.ChangePassword.as_view(), name='change'),
]
