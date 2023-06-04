import pytest
from routing.planner.models_to_graph import Waypoint


@pytest.fixture
def routing_graph():
    return {
        1: {2: [2],
            3: [1, 5],
            5: [10]},
        2: {1: [1],
            4: [3]},
        3: {6: [7],
            1: [1]},
        4: {5: [5],
            6: [4]},
        5: {},
        6: {4: [4],
            7: [9],
            1: [2],
            3: [7]},
        7: {6: [9]}
    }


@pytest.fixture
def restore_graph():
    return {
        1: {2: [1],
            3: [2, 11],
            5: [14]},
        2: {1: [3],
            4: [4]},
        3: {6: [5],
            1: [12]},
        4: {5: [6],
            6: [7]},
        5: {},
        6: {4: [8],
            7: [9],
            1: [13]},
        7: {6: [10]}
    }


@pytest.fixture
def waypoints():
    return {
        1: Waypoint(
            id=1, connection_id=1, cron='0 * * * *',  # every hour
            trip_time=2, time_from_first_station=12
        ),
        2: Waypoint(
            id=2, connection_id=2, cron='0 0 * * *',  # every day at 00:00
            trip_time=1, time_from_first_station=34
        ),
        3: Waypoint(
            id=3, connection_id=1, cron='30 3 * * *',  # every day at 3:30 AM
            trip_time=1, time_from_first_station=5
        ),
        4: Waypoint(
            id=4, connection_id=1, cron='0 9 * * 1',  # every Monday at 9:00 AM
            trip_time=3, time_from_first_station=21
        ),
        5: Waypoint(
            id=5, connection_id=2, cron='*/15 * * * *',  # every 15 minutes
            trip_time=7, time_from_first_station=17
        ),
        6: Waypoint(
            id=6, connection_id=1, cron='30 8 * * 1-5',  # every weekday at 8:30 AM
            trip_time=7, time_from_first_station=15
        ),
        7: Waypoint(
            id=7, connection_id=4, cron='*/5 * * * *',  # every 5 seconds
            trip_time=4, time_from_first_station=7
        ),
        8: Waypoint(
            id=8, connection_id=4, cron='30 4 1 * *',  # every 1st of the month at 4:30 AM
            trip_time=4, time_from_first_station=0
        ),
        9: Waypoint(
            id=9, connection_id=2, cron='*/5 * * * 1-5',  # every 5 minutes on weekdays
            trip_time=9, time_from_first_station=5
        ),
        10: Waypoint(
            id=10, connection_id=2, cron='0 22 * * 6',   # every Saturday at 10:00 PM
            trip_time=9, time_from_first_station=12
        ),
        11: Waypoint(
            id=11, connection_id=3, cron='0 22 * * 6',  # every Saturday at 10:00 PM
            trip_time=5, time_from_first_station=20
        ),
        12: Waypoint(
            id=12, connection_id=2, cron='0 * * * *',  # every hour
            trip_time=2, time_from_first_station=23
        ),
        13: Waypoint(
            id=13, connection_id=5, cron='*/15 * * * *',  # every 15 minutes
            trip_time=7, time_from_first_station=12
        ),
        14: Waypoint(
            id=14, connection_id=6, cron='*/5 * * * 1-5',  # every 5 minutes on weekdays
            trip_time=13, time_from_first_station=0
        ),
    }
