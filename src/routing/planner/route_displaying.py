from collections import namedtuple
from routing.planner.scheduled_route_finder import ScheduledRouteFinder

from datetime import datetime
from routing.planner.yen_algorithm import yen_algorithm

ScheduledConnection = namedtuple('ScheduledConnection',
                                 'station_id connection_id departure_from_stop arrival_to_next_stop')


class ScheduledRoute:
    scheduled_connection: [ScheduledConnection] = []

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

    scheduled_routes: [ScheduledRoute] = []

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
        return sorted(self.scheduled_routes, key=(lambda conn: conn.scheduled_connection[-1].arrival_to_next_stop))

    def __call__(self, search_time: datetime, *args, **kwargs):
        return self._order_routes_by_schedule(search_time)
