from datetime import datetime
import pytest

from routing.planner.scheduled_route_finder import ScheduledRouteFinder


@pytest.fixture
def scheduled_route_finder(restore_graph, waypoints):
    return ScheduledRouteFinder(restore_graph, waypoints)


def test_route_with_transfer_options(scheduled_route_finder):
    route = scheduled_route_finder([1, 3, 6, 7], datetime(2023, 4, 24, 16, 0, 0))
    assert len(route) == 3
    assert route == {
        1: {'arrival_time': datetime(2023, 4, 25, 0, 35),
              'departure_time': datetime(2023, 4, 25, 0, 34),
              'connection_id': 2},
        3: {'arrival_time': datetime(2023, 4, 25, 0, 54),
              'departure_time': datetime(2023, 4, 25, 0, 47),
              'connection_id': 2},
        6: {'arrival_time': datetime(2023, 4, 25, 1, 4),
              'departure_time': datetime(2023, 4, 25, 0, 55),
              'connection_id': 2}
    }


def test_route_without_transfer(scheduled_route_finder):
    route = scheduled_route_finder([1, 2], datetime(2023, 4, 24, 16, 0))
    assert len(route) == 1
    assert route == {1: {'arrival_time': datetime(2023, 4, 24, 16, 14),
                           'departure_time': datetime(2023, 4, 24, 16, 12),
                           'connection_id': 1}}


def test_not_enough_nodes(scheduled_route_finder):
    with pytest.raises(ValueError):
        scheduled_route_finder([], datetime(2023, 4, 24, 16, 0))
    with pytest.raises(ValueError):
        scheduled_route_finder([1], datetime(2023, 4, 24, 16, 0))
