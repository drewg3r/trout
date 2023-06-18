from typing import Self

from django.conf import settings
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64, verbose_name='назва')

    class Meta:
        verbose_name = 'місто'
        verbose_name_plural = 'міста'

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=64, verbose_name='назва')
    city = models.ForeignKey(to=City, on_delete=models.PROTECT, related_name='stations', verbose_name='місто')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='довгота')
    disabled = models.BooleanField(default=False, verbose_name='тимчасово недоступна')

    class Meta:
        verbose_name = 'станція'
        verbose_name_plural = 'станції'
        ordering = ('city__name', 'name')

    def __str__(self):
        return f'{self.city}: {self.name}'

    @property
    def osm_coordinates(self) -> str:
        return f'{self.latitude},{self.longitude}'

    @property
    def osm_bbox_coordinates(self) -> str:
        zoom = settings.OSM_ZOOM
        return f'{round(float(self.longitude) - zoom, 5)},' \
               f'{round(float(self.latitude) - zoom, 5)},' \
               f'{round(float(self.longitude) + zoom, 5)},' \
               f'{round(float(self.latitude) + zoom, 5)}'


class Route(models.Model):
    name = models.CharField(max_length=64, verbose_name='назва')

    class Meta:
        verbose_name = 'маршрут'
        verbose_name_plural = 'маршрути'

    def __str__(self):
        return self.name


class Waypoint(models.Model):
    station = models.ForeignKey(to=Station, on_delete=models.CASCADE, related_name='waypoints', verbose_name='станція')
    connection = models.ForeignKey(to='Connection', on_delete=models.CASCADE, related_name='waypoints', verbose_name='сполучення')
    trip_time = models.IntegerField(verbose_name='час в дорозі')
    disabled = models.BooleanField(default=False, verbose_name='тимчасово недоступна')

    class Meta:
        verbose_name = 'проміжна зупинка'
        verbose_name_plural = 'проміжні зупинки'

    def __str__(self):
        return f'{self.connection} to {self.station}'

    @property
    def next(self) -> Self:
        """Get next waypoint down the Connection"""
        return self.connection.waypoints.all() \
            .filter(trip_time__gt=self.trip_time).order_by('trip_time').first()

    @property
    def prev(self) -> Self:
        """Get previous waypoint in the Connection"""
        return self.connection.waypoints.all() \
            .filter(trip_time__lt=self.trip_time).order_by('trip_time').last()

    @property
    def adjacent_waypoints(self) -> tuple[Self]:
        return tuple(wp for wp in (self.next, self.prev) if wp is not None)


class Connection(models.Model):
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name='connections', verbose_name='маршрут')
    name = models.CharField(max_length=64, verbose_name='назва')
    departure_cron = models.CharField(max_length=64, verbose_name='розклад відправлення')
    disabled = models.BooleanField(default=False, verbose_name='тимчасово недоступнe')

    class Meta:
        verbose_name = 'сполучення'
        verbose_name_plural = 'сполучення'

    def __str__(self):
        return f'{self.route.name}: {self.name}'

    @staticmethod
    def trip_time_between(origin: Waypoint, destination: Waypoint) -> int:
        if origin.connection != destination.connection:
            raise ValueError('Both origin and destination should belong to one Connection')
        return abs(origin.trip_time - destination.trip_time)

    @property
    def end_station(self):
        return self.waypoints.all().order_by('trip_time').last().station
