import django_filters

from bars_calculation.models import CalculationRhs
from distance_checker.models import Corner, Ridge


class CornerFilter(django_filters.FilterSet):
    class Meta:
        model = Corner
        fields = {'case': ["icontains"]}


class RidgeFilter(django_filters.FilterSet):
    class Meta:
        model = Ridge
        fields = {'case': ["icontains"]}


class CalculationRhsFilter(django_filters.FilterSet):
    class Meta:
        model = CalculationRhs
        fields = {'case': ["icontains"]}
