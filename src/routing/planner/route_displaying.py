from typing import NamedTuple

from main.models import Station
from routing.planner.datatypes import Route, DirectLine, Waypoint
from routing.planner.scheduled_route_finder import ScheduledRouteFinder

from datetime import datetime
from routing.planner.yen_algorithm import yen_algorithm
from routing.planner.models_to_graph import create_search_data


class ScheduledConnection(NamedTuple):
    """
    Attributes:
        station_id: database id of the Station that relates to
            this ScheduledConnection
        connection_id: ???
        departure_time: Departure time from THIS station (self.station_id)
        arrival_time: Arrival time to NEXT station (cannot be retrieved from this class instance)
    """
    station_id: int
    connection_id: int
    departure_time: datetime
    arrival_time: datetime


class ScheduledRoute:
    scheduled_connection: list[ScheduledConnection]

    def __init__(self, restore_graph: dict, waypoints: dict, route: list[int], search_time: datetime):
        self.restore_graph = restore_graph
        self.waypoints = waypoints

        self._find_scheduled_route(route, search_time)

    def _find_scheduled_route(self, route: list, search_time: datetime) -> [ScheduledConnection]:
        self.scheduled_connection = []
        route_finder = ScheduledRouteFinder(self.restore_graph, self.waypoints)
        scheduled_route = route_finder(route, search_time)
        for station in route:
            if station in scheduled_route:
                self.scheduled_connection.append(ScheduledConnection(
                    station,
                    scheduled_route[station]['connection_id'],
                    scheduled_route[station]['departure_time'],
                    scheduled_route[station]['arrival_time']
                ))

    def __eq__(self, other):
        return self.scheduled_connection == other


class BestScheduledRoutes:
    scheduled_routes: list[ScheduledRoute]

    def __init__(self, start_station_id: int, end_station_id: int, graph: dict, restore_graph: dict,
                 waypoints: dict):
        if start_station_id not in graph or end_station_id not in graph:
            raise ValueError(f'Start station ({start_station_id}) and end station ({end_station_id})'
                             f' should be in routing graph {graph}')
        self.start_station_id = start_station_id
        self.end_station_id = end_station_id
        self.graph = graph
        self.restore_graph = restore_graph
        self.waypoints = waypoints

    def _order_routes_by_schedule(self, search_time):
        self.scheduled_routes = []
        routes = yen_algorithm(self.graph, self.start_station_id, self.end_station_id)
        # routes_with_schedule = []
        for route in routes:
            scheduled_route = ScheduledRoute(self.restore_graph, self.waypoints, route, search_time)
            self.scheduled_routes.append(scheduled_route)
        return sorted(self.scheduled_routes, key=(lambda conn: conn.scheduled_connection[-1].arrival_time))

    def find_several_best_routes(self, search_time: datetime):
        return self._order_routes_by_schedule(search_time)

    def find_one_best_route(self, search_time: datetime):
        return self.find_several_best_routes(search_time)[0]


def find_route(start_station_id: int, end_station_id: int, search_time: datetime, dry_run: bool = False):
    """
    Main function of this app
    finds best route between given stations
    and finds the best departure time based on search_time
    Args:
        start_station_id: id of station from which user wants to depart
        end_station_id: id of station to which user wants to get
        search_time: time when user wants to depart from start station
        dry_run: return fixture data instead of real route

    Returns:
        best route existing with scheduled departure time
    """
    if dry_run:
        return route_example

    routing_graph, restore_graph, waypoints = create_search_data()
    best_route = BestScheduledRoutes(
        start_station_id=start_station_id,
        end_station_id=end_station_id,
        graph=routing_graph,
        restore_graph=restore_graph,
        waypoints=waypoints
    )

    return best_route.find_one_best_route(search_time)


route_example = Route(
    origin=Station.objects.get(id=5),
    destination=Station.objects.get(id=2),
    departure_time=datetime(2023, 5, 12, 16, 1),
    direct_lines=[
        DirectLine(
            name='A51',
            end_station=Station.objects.get(id=1),
            waypoints=[
                Waypoint(Station.objects.get(id=5), datetime(2023, 5, 14, 16, 7), datetime(2023, 5, 14, 16, 8)),
                Waypoint(Station.objects.get(id=13), datetime(2023, 5, 14, 16, 14), datetime(2023, 5, 14, 16, 15)),
                Waypoint(Station.objects.get(id=1), datetime(2023, 5, 14, 16, 24), datetime(2023, 5, 14, 16, 25)),
            ],
        ),
        DirectLine(
            name='A230',
            end_station=Station.objects.get(id=2),
            waypoints=[
                Waypoint(Station.objects.get(id=1), datetime(2023, 5, 14, 16, 37), datetime(2023, 5, 14, 16, 38)),
                Waypoint(Station.objects.get(id=7), datetime(2023, 5, 14, 16, 53), datetime(2023, 5, 14, 16, 55)),
                Waypoint(Station.objects.get(id=8), datetime(2023, 5, 14, 17, 3), datetime(2023, 5, 14, 17, 4)),
                Waypoint(Station.objects.get(id=9), datetime(2023, 5, 14, 17, 10), datetime(2023, 5, 14, 17, 11)),
                Waypoint(Station.objects.get(id=10), datetime(2023, 5, 14, 17, 15), datetime(2023, 5, 14, 17, 18)),
                Waypoint(Station.objects.get(id=12), datetime(2023, 5, 14, 19, 14), datetime(2023, 5, 14, 19, 20)),
                Waypoint(Station.objects.get(id=11), datetime(2023, 5, 14, 19, 30), datetime(2023, 5, 14, 19, 31)),
                Waypoint(Station.objects.get(id=2), datetime(2023, 5, 14, 19, 37), datetime(2023, 5, 14, 19, 36)),
            ],
        ),
    ]
)