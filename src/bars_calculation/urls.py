from django.urls import path

from .views import CalculationRhsView

urlpatterns = [
    path('', CalculationRhsView.as_view(), name='calculation_bar'),
]
