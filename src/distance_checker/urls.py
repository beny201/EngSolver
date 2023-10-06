from django.urls import path, include
from .views import BasicView, DistanceView

urlpatterns = [
    path('', BasicView.as_view(), name='index'),
    path('frame_corner', DistanceView.as_view(), name='corner_distance'),
    path('frame_ridge', DistanceView.as_view(), name='ridge_distance'),
]