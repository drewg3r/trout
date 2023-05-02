from typing import NamedTuple
from main import models
from itertools import tee, groupby


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Waypoint(NamedTuple):
    """
    A class for the Waypoint from models
    Attributes:
        id: the id of waypoint
        connection_id: the id of connection that has waypoint
        cron: cron of a connection's departure time
        trip_time: time to travel between stations
        time_from_first_station: time from connection's departure to station
    """
    id: int
    connection_id: int
    cron: str
    trip_time: int
    time_from_first_station: int


def create_graph_nodes() -> dict:
    routing_graph = {}
    stations = models.Station.objects.all()
    for station in stations:
        routing_graph[station.id] = {}
    return routing_graph


def create_graph_edges(routing_graph):
    waypoints = models.Waypoint.objects.all()
    waypoints_dict = {}
    restore_graph = {}
    key_func_connection = lambda x: x.connection_id
    key_func_time = lambda x: x.trip_time
    waypoints_sorted = sorted(waypoints, key=key_func_connection)
    waypoints_grouped = groupby(waypoints_sorted, key_func_connection)
    for key, group in waypoints_grouped:
        group = sorted(group, key=key_func_time)
        for waypoint1, waypoint2 in pairwise(group):
            routing_graph[waypoint1.station.id][waypoint2.station.id] = (waypoint2.trip_time - waypoint1.trip_time)
            if waypoint1.station.id not in restore_graph:
                restore_graph[waypoint1.station.id] = {waypoint2.station.id: waypoint2.id}
            else:
                restore_graph[waypoint1.station.id][waypoint2.station.id] = waypoint2.id
            waypoint = Waypoint(
                id=waypoint2.id,
                connection_id=waypoint2.connection.id,
                cron=waypoint2.connection.departure_cron,
                trip_time=(waypoint2.trip_time - waypoint1.trip_time),
                time_from_first_station=waypoint2.trip_time
            )
            waypoints_dict[waypoint2.id] = waypoint
    return routing_graph, restore_graph, waypoints_dict


def create_graph():
    routing_graph = create_graph_nodes()
    routing_graph, restore_graph, waypoints = create_graph_edges(routing_graph)
    return routing_graph, restore_graph, waypoints



routing_graph = {
    '1': {'2': [2],
          '3': [1, 5],
          '5': [10]},
    '2': {'1': [1],
          '4': [3]},
    '3': {'6': [7],
          '1': [1]},
    '4': {'5': [5],
          '6': [4]},
    '5': {},
    '6': {'4': [4],
          '7': [9],
          '1': [2],
          '3': [7]},
    '7': {'6': [9]}
}

# dictionary used to restore waypoints from graph
# (1) -waypoint-> (2)
restore_graph = {
        '1': {'2': [1],
              '3': [2, 11],
              '5': [14]},
        '2': {'1': [3],
              '4': [4]},
        '3': {'6': [5],
              '1': [12]},
        '4': {'5': [6],
              '6': [7]},
        '5': {},
        '6': {'4': [8],
              '7': [9],
              '1': [13]},
        '7': {'6': [10]}
    }

waypoints = {
    1: Waypoint(id=1,   connection_id=1, cron='0 * * * *',     trip_time=2, time_from_first_station=12),  # every hour
    2: Waypoint(id=2,   connection_id=2, cron='0 0 * * *',     trip_time=1, time_from_first_station=34),  # every day at 00:00
    3: Waypoint(id=3,   connection_id=1, cron='30 3 * * *',    trip_time=1, time_from_first_station=5),  # every day at 3:30 AM
    4: Waypoint(id=4,   connection_id=1, cron='0 9 * * 1',     trip_time=3, time_from_first_station=21),  # every Monday at 9:00 AM
    5: Waypoint(id=5,   connection_id=2, cron='*/15 * * * *',  trip_time=7, time_from_first_station=17),  # every 15 minutes
    6: Waypoint(id=6,   connection_id=1, cron='30 8 * * 1-5',  trip_time=7, time_from_first_station=15),  # every weekday at 8:30 AM
    7: Waypoint(id=7,   connection_id=4, cron='*/5 * * * *',   trip_time=4, time_from_first_station=7),  # every 5 seconds
    8: Waypoint(id=8,   connection_id=4, cron='30 4 1 * *',    trip_time=4, time_from_first_station=0),  # every 1st of the month at 4:30 AM
    9: Waypoint(id=9,   connection_id=2, cron='*/5 * * * 1-5', trip_time=9, time_from_first_station=5),  # every 5 minutes on weekdays
    10: Waypoint(id=10, connection_id=2, cron='0 22 * * 6',    trip_time=9, time_from_first_station=12),  # every Saturday at 10:00 PM
    11: Waypoint(id=11, connection_id=3, cron='0 22 * * 6',    trip_time=5, time_from_first_station=20),  # every Saturday at 10:00 PM
    12: Waypoint(id=12, connection_id=2, cron='0 * * * *',     trip_time=2, time_from_first_station=23),  # every hour
    13: Waypoint(id=13, connection_id=5, cron='*/15 * * * *',  trip_time=7, time_from_first_station=12),  # every 15 minutes
    14: Waypoint(id=14, connection_id=6, cron='*/5 * * * 1-5', trip_time=13, time_from_first_station=0),  # every 5 minutes on weekdays
}
