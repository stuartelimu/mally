from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Store, Area

@admin.register(Store)
class StoreAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')


@admin.register(Area)
class AreaAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')


