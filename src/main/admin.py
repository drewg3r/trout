from django.contrib import admin

from main.models import City, Station


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass
