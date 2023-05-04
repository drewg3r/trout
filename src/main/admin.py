from django.contrib import admin

from main.models import City, Station, Route, Connection, Waypoint


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass


class WaypointInline(admin.TabularInline):
    model = Waypoint
    extra = 3


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    inlines = [WaypointInline]


@admin.register(Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    pass
