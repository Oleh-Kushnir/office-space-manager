from django.contrib import admin
from .models import Building, Room, Tenant, Lease, Tariff, UtilityReading

# Register your models here.
@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('utility_type', 'price_per_unit', 'effective_from')
    list_filter = ('utility_type',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(UtilityReading)
class UtilityReadingAdmin(admin.ModelAdmin):
    list_display = ('utility_type', 'room', 'reading_date', 'value', 'consumption', 'cost')
    list_filter = ('utility_type',)


admin.site.register(Building)
admin.site.register(Tenant)
admin.site.register(Lease)

