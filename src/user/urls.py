from django.urls import path, include
from .views import register

urlpatterns = [
    path('', register , name='register'),
]