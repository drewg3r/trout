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
    """
    Reads stations from database and creates node
    in graph with station's id

    Returns:
        a graph that contains only nodes
    """
    routing_graph = {}
    stations = models.Station.objects.all()
    for station in stations:
        routing_graph[station.id] = {}
    return routing_graph


def create_graph_data(routing_graph):
    """
    reads data from Waypoints table in database
    and creates all data structures needed to find a route
    Args:
        routing_graph: a graph that contains nodes(Stations)

    Returns:
        routing_graph: a dict used to find routes, contains all stations and connections between them
        restore_graph: a dict used to restore waypoint between stations by their id
        waypoints: a dict with all data about waypoints needed to find schedules
    """
    waypoints = models.Waypoint.objects.all()
    waypoints_dict = {}
    restore_graph = {}
    waypoints_sorted = sorted(waypoints, key=lambda x: x.connection_id)
    waypoints_grouped = groupby(waypoints_sorted, lambda x: x.connection_id)
    for key, group in waypoints_grouped:
        group = sorted(group, key=lambda x: x.trip_time)
        for waypoint1, waypoint2 in pairwise(group):
            routing_graph[waypoint1.station.id][waypoint2.station.id] = (waypoint2.trip_time - waypoint1.trip_time)
            if waypoint1.station.id not in restore_graph or waypoint2.station.id not in restore_graph[waypoint1.station.id]:
                restore_graph[waypoint1.station.id] = {waypoint2.station.id: [waypoint2.id]}
            else:
                restore_graph[waypoint1.station.id][waypoint2.station.id].append(waypoint2.id)
            waypoint = Waypoint(
                id=waypoint2.id,
                connection_id=waypoint2.connection.id,
                cron=waypoint2.connection.departure_cron,
                trip_time=(waypoint2.trip_time - waypoint1.trip_time),
                time_from_first_station=waypoint2.trip_time
            )
            waypoints_dict[waypoint2.id] = waypoint
    return routing_graph, restore_graph, waypoints_dict


def create_search_data():
    """
    Reads data needed to find routes and transforms it
    to correct datatypes
    Returns:
        routing_graph: a dict used to find routes, contains all stations and connections between them
        restore_graph: a dict used to restore waypoint between stations by their id
        waypoints: a dict with all data about waypoints needed to find schedules
    """
    routing_graph = create_graph_nodes()
    routing_graph, restore_graph, waypoints = create_graph_data(routing_graph)
    return routing_graph, restore_graph, waypoints
