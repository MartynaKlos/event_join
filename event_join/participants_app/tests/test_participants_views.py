import pytest

from events_app.models import Event
from participants_app.models import Participant


@pytest.mark.django_db
def test_register(set_up, client):
    event = Event.objects.filter(is_private=False).order_by('?').first()
    participants_count = Participant.objects.count()
    url = f'/events/register/{event.pk}/'
    data = {
        'name': 'Participant',
        'surname': 'New',
        'email': 'new_participant@gmail.com',
        'event': event.pk
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert Participant.objects.count() == participants_count + 1


@pytest.mark.django_db
def test_email_confirmation(set_up, client):
    participant = Participant.objects.all().order_by('?').first()
    breakpoint()
    url = f'/participant/email/{participant.confirmation_id}/'
    response = client.get(url)
    assert response.status_code == 200
    confirmed = participant.is_confirmed
    assert confirmed is True


@pytest.mark.django_db
def test_accept_invite(set_up, client):
    participant = Participant.objects.all().order_by('?').first()
    url = f'/participant/invite/{participant.accepted_id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert participant.is_active is True


@pytest.mark.django_db
def test_decline_invite(set_up, client):
    participant = Participant.objects.all().order_by('?').first()
    url = f'/participant/invite/{participant.declined_id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert participant.is_active is False
