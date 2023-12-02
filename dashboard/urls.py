from django.urls import path

from dashboard.views import (
    BarCalculationView,
    BarDeleteView,
    BarDetailedView,
    CalculationsView,
    CornerCalculationView,
    CornerDeleteView,
    CornerDetailedView,
    RidgeCalculationView,
    RidgeDeleteView,
    RidgeDetailedView,
)

urlpatterns = [
    path('', CalculationsView.as_view(), name='dashboard'),
    path('connections/corner/', CornerCalculationView.as_view(), name='corner_view'),
    path(
        'connections/corner/<int:pk>',
        CornerDetailedView.as_view(),
        name='corner_detail',
    ),
    path(
        'connections/corner/<int:pk>/delete',
        CornerDeleteView.as_view(),
        name='corner_delete',
    ),
    path('connections/ridge/', RidgeCalculationView.as_view(), name='ridge_view'),
    path(
        'connections/ridge/<int:pk>', RidgeDetailedView.as_view(), name='ridge_detail'
    ),
    path(
        'connections/ridge/<int:pk>/delete',
        RidgeDeleteView.as_view(),
        name='ridge_delete',
    ),
    path('connections/bar/', BarCalculationView.as_view(), name='bars_view'),
    path(
        'connections/bar/<int:pk>/delete',
        BarDeleteView.as_view(),
        name='bar_delete',
    ),
    path(
        'connections/bar/<int:pk>',
        BarDetailedView.as_view(),
        name='bar_detail',
    ),
]
