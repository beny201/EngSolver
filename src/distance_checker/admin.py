from django.contrib import admin

# Register your models here.

from .models import BoltStandard, WasherStandard, NutStandard, Bolt, Washer, Nut


admin.site.register(BoltStandard)
admin.site.register(WasherStandard)
admin.site.register(NutStandard)
admin.site.register(Bolt)
admin.site.register(Washer)
admin.site.register(Nut)