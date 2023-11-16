from django.contrib import admin

from .models import CalculationCfrhs, DetailedCalculationCfrhs, ProfileRhs

admin.site.register(ProfileRhs)
admin.site.register(CalculationCfrhs)
admin.site.register(DetailedCalculationCfrhs)
