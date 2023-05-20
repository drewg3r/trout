from datetime import datetime, timedelta
from typing import NamedTuple

from main.models import Station


class Waypoint(NamedTuple):
    """
    Represents a Station on DirectLine.

    Attributes:
        station: Station that the Waypoint represents
        arrival_time: time when transport arrives to the Station
        departure_time: time when transport leaves the Station
    """
    station: Station
    arrival_time: datetime
    departure_time: datetime


class DirectLine(NamedTuple):
    """
    Represents *direct* line as a part of requested Route.

    Attributes:
        name: name of the line (e.g. 'M3').
        end_station: end Station of this line (not the last waypoint). Needed
            to get direction of this DirectLine (e.g. 'M3 -> Bilk S')
        waypoints: list of Stations to pass on this direct line. Sorted by
            arrival time on every Station along the Route.
    """
    name: str
    end_station: Station
    waypoints: list[Waypoint]

    @property
    def first_waypoint(self) -> Waypoint:
        return self.waypoints[0]

    @property
    def last_waypoint(self) -> Waypoint:
        return self.waypoints[-1]

    @property
    def travel_time(self) -> timedelta:
        """Time spent on this DirectLine"""
        return self.last_waypoint.arrival_time - self.first_waypoint.departure_time

    @property
    def intermediate_waypoints(self) -> list[Waypoint | None]:
        """Intermediate waypoints (i.e. not used to transfer to another line)"""
        return self.waypoints[1:-1]


class Route(NamedTuple):
    """
    Represents requested route between origin and destination at specific time.

    Attributes:
        origin: start Station the Route begins at
        destination: end Station of the Route
        departure_time: requested departure time form origin
        direct_lines: list of *direct* lines one should use to get from origin
            to destination.
    """
    origin: Station
    destination: Station
    departure_time: datetime
    direct_lines: list[DirectLine]

    @property
    def arrival_waypoint(self) -> Waypoint:
        return self.direct_lines[0].first_waypoint

    @property
    def destination_waypoint(self) -> Waypoint:
        return self.direct_lines[-1].last_waypoint

    @property
    def origin_departure_time(self) -> datetime:
        """Calculated departure time from origin"""
        return self.arrival_waypoint.departure_time

    @property
    def destination_arrival_time(self) -> datetime:
        """Calculated arrival time to destination"""
        return self.destination_waypoint.arrival_time

    @property
    def travel_time(self) -> timedelta:
        return self.destination_arrival_time - self.origin_departure_time