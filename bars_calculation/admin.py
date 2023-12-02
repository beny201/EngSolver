from django.contrib import admin

from .models import CalculationRhs, DetailedCalculationRhs, ProfileRhs

admin.site.register(ProfileRhs)
admin.site.register(CalculationRhs)
admin.site.register(DetailedCalculationRhs)
