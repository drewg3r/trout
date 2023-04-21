from django.urls import reverse_lazy


def test_index_view(client):
    response = client.get(reverse_lazy('index'))
    assert response.status_code == 200
