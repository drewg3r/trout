from datetime import datetime
import pytest

from routing.planner.route_displaying import BestScheduledRoutes, ScheduledConnection


def test_start_equals_end(routing_graph, restore_graph, waypoints):
    scheduled_route = BestScheduledRoutes(1, 1, routing_graph, restore_graph, waypoints)
    with pytest.raises(ValueError):
        scheduled_route(datetime(2023, 4, 24, 16, 0))
    with pytest.raises(ValueError):
        scheduled_route(datetime(2023, 4, 24, 16, 0))


def test_start_not_in_graph(routing_graph, restore_graph, waypoints):
    with pytest.raises(ValueError):
        BestScheduledRoutes(20, 2, routing_graph, restore_graph, waypoints)


def test_end_not_in_graph(routing_graph, restore_graph, waypoints):
    with pytest.raises(ValueError):
        BestScheduledRoutes(2, 20, routing_graph, restore_graph, waypoints)


def test_route_without_transfer(routing_graph, restore_graph, waypoints):
    scheduled_route = BestScheduledRoutes(1, 2, routing_graph, restore_graph, waypoints)
    routes = [[
        ScheduledConnection(1, 1, datetime(2023, 4, 24, 16, 12), datetime(2023, 4, 24, 16, 14))
    ]]
    assert routes == scheduled_route(datetime(2023, 4, 24, 16, 0))


def test_route_from_1_to_5(routing_graph, restore_graph, waypoints):
    scheduled_route = BestScheduledRoutes(1, 5, routing_graph, restore_graph, waypoints)
    routes = [
        [
            ScheduledConnection(1, 6, datetime(2023, 4, 24, 16, 5), datetime(2023, 4, 24, 16, 18))
        ],
        [
            ScheduledConnection(1, 2, datetime(2023, 4, 25, 8, 34), datetime(2023, 4, 25, 8, 35)),
            ScheduledConnection(3, 2, datetime(2023, 4, 25, 8, 47), datetime(2023, 4, 25, 8, 54)),
            ScheduledConnection(6, 4, datetime(2023, 4, 25, 9, 30), datetime(2023, 4, 25, 9, 34)),
            ScheduledConnection(4, 1, datetime(2023, 4, 25, 9, 35), datetime(2023, 4, 25, 9, 42))
        ],
        [
            ScheduledConnection(1, 1, datetime(2023, 4, 24, 16, 12), datetime(2023, 4, 24, 16, 14)),
            ScheduledConnection(2, 1, datetime(2023, 5, 1, 9, 21), datetime(2023, 5, 1, 9, 24)),
            ScheduledConnection(4, 1, datetime(2023, 5, 1, 9, 35), datetime(2023, 5, 1, 9, 42))
        ]
    ]
    assert routes == scheduled_route(datetime(2023, 4, 24, 16, 0))
