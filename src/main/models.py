from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64)


class Route(models.Model):
    name = models.CharField(max_length=64)


class Connection(models.Model):
    name = models.CharField(max_length=64)
    departure_cron = models.CharField(max_length=64)
    disabled = models.BooleanField(default=False)
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name='connections')


class Station(models.Model):
    name = models.CharField(max_length=64)
    city = models.ForeignKey(to=City, on_delete=models.PROTECT, related_name='stations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Waypoint(models.Model):
    station = models.ForeignKey(to=Station, on_delete=models.CASCADE, related_name='waypoints')
    connection = models.ForeignKey(to=Connection, on_delete=models.CASCADE, related_name='waypoints')
    trip_time = models.IntegerField()
    disabled = models.BooleanField(default=False)
