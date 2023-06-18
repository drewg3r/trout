from datetime import datetime
from typing import NamedTuple

from main.models import Station, Waypoint, Connection
from routing.planner import datatypes
from routing.planner.yen_algorithm import yen_algorithm


class AdjacentWaypoint(NamedTuple):
    base: Waypoint
    adjacent: Waypoint


class AdjacentStations:
    def __init__(self, base_station: Station):
        self.base_station = base_station
        self.adjacent_waypoints: list[AdjacentWaypoint] = []

        for waypoint in base_station.waypoints.all():
            for adjacent_waypoint in waypoint.adjacent_waypoints:
                self.adjacent_waypoints.append(AdjacentWaypoint(base=waypoint, adjacent=adjacent_waypoint))

    def as_dict(self):
        station_ids = [waypoint.adjacent.station.id for waypoint in self.adjacent_waypoints]
        adjacent_stations_dict = {k: [] for k in station_ids}

        for base_waypoint, adjacent_waypoint in self.adjacent_waypoints:
            adjacent_stations_dict[adjacent_waypoint.station.id].append(
                (Connection.trip_time_between(base_waypoint, adjacent_waypoint), (base_waypoint, adjacent_waypoint))
            )

        return adjacent_stations_dict


class RoutingGraph:
    """Internal data structure for yen algorithm to work with"""
    def __init__(self):
        self.stations_graph = dict()
        for station in Station.objects.all():
            self.stations_graph.update({station.id: AdjacentStations(station).as_dict()})

    def as_dict(self):
        return self.stations_graph


class RouteFinder:
    def __init__(self):
        self.routing_graph = RoutingGraph()

    def find_route(self, origin: Station, destination: Station, departure_time: datetime) -> datatypes.Route:
        yen_route = yen_algorithm(self.routing_graph.as_dict(), origin.id, destination.id)[0][1][1:]

        direct_lines: list[datatypes.DirectLine] = []

        # waypoints: list[Waypoint] = [datatypes.Waypoint(
        #     station=yen_route[0][1].station,
        #     arrival_time=datetime.now(),
        #     departure_time=datetime.now(),
        # )]

        waypoints: list[Waypoint] = [datatypes.Waypoint(
            station=yen_route[0][0].station,
            arrival_time=datetime.now(),
            departure_time=datetime.now(),
        ), datatypes.Waypoint(
            station=yen_route[0][1].station,
            arrival_time=datetime.now(),
            departure_time=datetime.now(),
        )]

        last_waypoint: Waypoint = yen_route[0][1]

        # TODO: fix arrival departure time
        for waypoint1, waypoint2 in yen_route[1:]:

            if last_waypoint.connection.route == waypoint1.connection.route:
                waypoints.append(datatypes.Waypoint(
                    station=waypoint2.station,
                    arrival_time=datetime.now(),
                    departure_time=datetime.now(),
                ))
            else:
                # TODO: fix end station
                direct_lines.append(datatypes.DirectLine(
                    name=waypoint1.connection.route.name,
                    end_station=waypoint1.connection.end_station,
                    waypoints=waypoints
                ))
                waypoints = [datatypes.Waypoint(
                    station=waypoint1.station,
                    arrival_time=datetime.now(),
                    departure_time=datetime.now(),
                ), datatypes.Waypoint(
                    station=waypoint2.station,
                    arrival_time=datetime.now(),
                    departure_time=datetime.now(),
                )]
                last_waypoint = waypoint2

        if waypoints:
            direct_lines.append(datatypes.DirectLine(
                name=yen_route[-1][1].connection.route.name,
                end_station=yen_route[-1][1].connection.end_station,
                waypoints=waypoints
            ))

        return datatypes.Route(origin=origin,
                               destination=destination,
                               departure_time=departure_time,
                               direct_lines=direct_lines)


# print(RouteFinder().find_route(origin=Station.objects.get(id=1), destination=Station.objects.get(id=8), departure_time=datetime.now()))

rg = RoutingGraph()
print(rg.as_dict())
# print(yen_algorithm(rg.as_dict(), 1, 8))

# for w in found_route[0][1]:
#     if w:
#         print(w.id)
# print(rg.as_dict())

