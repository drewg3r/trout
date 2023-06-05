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
    autocomplete_fields = ('station',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    inlines = [StationInline]
    search_fields = ('name',)
    list_display = ('name', 'stations_amount')
    ordering = ('name',)

    @admin.display(description='Кількість станцій')
    def stations_amount(self, city):
        return city.stations.count()


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    ordering = ('city__name', 'name')
    list_display = ('name', 'city', 'id', 'active')
    search_fields = ('name', 'city__name')
    autocomplete_fields = ('city',)

    @admin.display(description='Активне', boolean=True)
    def active(self, station):
        return not station.disabled


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = [ConnectionInline]
    ordering = ('name',)
    list_display = ('name', 'connections_amount',)
    search_fields = ('name',)

    @admin.display(description='Кількість сполученнь')
    def connections_amount(self, route):
        return len(route.connections.all())


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    inlines = [WaypointInline]
    list_display = ('name', 'route', 'origin', 'destination', 'active')
    ordering = ('route',)
    search_fields = ('name', 'route__name')
    autocomplete_fields = ('route',)
    list_filter = ('disabled',)

    @admin.display(description='Відправлення')
    def origin(self, connection):
        return sorted(connection.waypoints.all(), key=lambda x: x.trip_time)[0].station

    @admin.display(description='Прибуття')
    def destination(self, connection):
        return sorted(connection.waypoints.all(), key=lambda x: x.trip_time)[-1].station

    @admin.display(description='Активне', boolean=True)
    def active(self, connection):
        return not connection.disabled


admin.site.site_title = "Trout"
admin.site.site_header = "Керування маршрутами"
admin.site.index_title = "Головна сторінка"