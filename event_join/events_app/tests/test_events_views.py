import random

import pytest
from random import randint

from events_app.models import Event
from events_app.tests.utils import set_random_date


@pytest.mark.django_db
def test_events_list_view(set_up, client):
    url = '/events/'
    response = client.get(url)
    list_view = list(response.context['events'].values_list('pk', flat=True))
    list_db = list(Event.objects.filter(is_private=False).values_list('pk', flat=True))
    assert response.status_code == 200
    assert list_db == list_view


@pytest.mark.django_db
def test_event_details_view(set_up, client):
    event = Event.objects.all().first()
    url = f'/events/{event.pk}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['title'] == event.title
    assert response.context['description'] == event.description
    assert response.context['limit'] == event.limit
    assert response.context['start_date'] == event.start_date
    assert response.context['is_private'] == event.is_private


@pytest.mark.django_db
def test_add_event_view(client):
    url = '/events/add_event/'
    data = {
        "title": 'nowy event',
        'description': 'To jest nowy event',
        'start_date': set_random_date(),
        'end_date': set_random_date(),
        'limit': randint(10, 100),
        'registration_start': set_random_date(),
        'registration_end': set_random_date(),
        'is_private': bool(random.getrandbits(1))
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Event.objects.all().count() == 1



