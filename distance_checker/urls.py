from django.urls import include, path

from .views import BasicView, DistanceCornerView, DistanceRidgeView

urlpatterns = [
    path('', BasicView.as_view(), name='index'),
    path('frame_corner', DistanceCornerView.as_view(), name='corner_distance'),
    path('frame_ridge', DistanceRidgeView.as_view(), name='ridge_distance'),
]
