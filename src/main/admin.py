from django.contrib import admin

from main.models import City, Station, Route, Connection, Waypoint


class StationInline(admin.TabularInline):
    model = Station
    extra = 0


class ConnectionInline(admin.TabularInline):
    model = Connection
    extra = 0


class WaypointInline(admin.TabularInline):
    model = Waypoint
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    inlines = [StationInline]


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = [ConnectionInline]


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    inlines = [WaypointInline]


@admin.register(Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    pass
