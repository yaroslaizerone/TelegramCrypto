from django.contrib import admin
from core.models import Person, PersonUsage, PersonTag, Region, Country, CryptoObject


class CryptoAdmin (admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Person)
admin.site.register(PersonUsage)
admin.site.register(PersonTag)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(CryptoObject, CryptoAdmin)