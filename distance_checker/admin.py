from django.contrib import admin

from .models import (
    Bolt,
    BoltStandard,
    Corner,
    Nut,
    NutStandard,
    Ridge,
    Washer,
    WasherStandard,
)

admin.site.register(BoltStandard)
admin.site.register(WasherStandard)
admin.site.register(NutStandard)
admin.site.register(Bolt)
admin.site.register(Washer)
admin.site.register(Nut)
admin.site.register(Corner)
admin.site.register(Ridge)
