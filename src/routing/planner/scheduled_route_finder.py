from math import inf
from datetime import datetime, timedelta
from croniter import croniter


class ScheduledRouteFinder:
    def __init__(self, restore_graph: dict, waypoints: dict):
        self.restore_graph = restore_graph
        self.waypoints = waypoints

    @staticmethod
    def next_cron(search_time, cron):
        return croniter(cron, search_time).get_next(datetime)

    @staticmethod
    def minutes_between_dates(date1, date2):
        return (date1 - date2).total_seconds() / 60

    def _find_travel_time(self, station_id: int, next_station_id: int, search_time: datetime) -> (int, datetime):
        """
        function that finds travel time to next station considering waiting time
        returns time in seconds
        """
        smallest_time = inf
        best_departure_time = 0
        best_arrival_time = 0
        best_waypoint = 0
        waypoints_id = self.restore_graph[station_id][next_station_id]
        for waypoint_id in waypoints_id:
            waypoint = self.waypoints[waypoint_id]
            travel_time = waypoint.trip_time
            departure_time = self.next_cron(search_time -
                                            timedelta(minutes=waypoint.time_from_first_station),
                                            waypoint.cron)
            departure_time += timedelta(minutes=waypoint.time_from_first_station)
            waiting_time = self.minutes_between_dates(departure_time, search_time)
            if (travel_time + waiting_time) < smallest_time:
                smallest_time = travel_time + waiting_time
                best_departure_time = departure_time
                best_arrival_time = departure_time + timedelta(minutes=travel_time)
                best_waypoint = waypoint
        return best_departure_time, best_arrival_time, best_waypoint

    def _find_scheduled_route(self, route: list, search_time: datetime) -> [tuple]:
        best_route = {}
        for node, next_node in ((route[i], route[i + 1]) for i in range(len(route) - 1)):
            departure_time, arrival_time, waypoint = self._find_travel_time(node, next_node, search_time)
            best_route[node] = {'departure_time': departure_time,
                                'arrival_time': arrival_time,
                                'connection_id': waypoint.connection_id}
            search_time = arrival_time
        return best_route

    def __call__(self, route: list, search_time: datetime, *args, **kwargs):
        if len(route) < 2:
            raise ValueError(f'Route should have at least 2 points: {route}')
        return self._find_scheduled_route(route, search_time)
