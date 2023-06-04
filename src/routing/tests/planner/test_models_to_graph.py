from routing.planner.models_to_graph import create_search_data


def test_create_search_data(db):
    create_search_data()
