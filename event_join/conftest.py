import random

from faker import Faker
import pytest
from random import randint

from events_app.models import Event
from events_app.tests.utils import set_random_date
from participants_app.models import Participant

faker = Faker("pl_PL")


@pytest.fixture
def set_up():
    for i in range(5):
        Event.objects.create(
            title=faker.word(),
            description=faker.text(max_nb_chars=100),
            start_date=set_random_date(),
            end_date=set_random_date(),
            limit=randint(10, 100),
            registration_start=set_random_date(),
            registration_end=set_random_date(),
            is_private=bool(random.getrandbits(1))
        )
    for i in range(10):
        Participant.objects.create(
            name=faker.name(),
            surname=faker.word(),
            email=faker.email(),
            event=Event.objects.all().order_by('?').first()
        )

