from routing.planner.models_to_graph import create_graph_edges
from main.models import Station, City


def test_add_data_to_db(db):
    c = City(name='C1')
    c.save()
    s1 = Station(name='St1', city_id=c.id, latitude='122334', longitude='12233')
    s2 = Station(name='St2', city_id=c.id, latitude='122334', longitude='12233')
    s1.save()
    s2.save()


def test_create_graph_edges(db):
    print("\n\n\n\n\n", create_graph_edges(), "\n\n\n\n\n")
