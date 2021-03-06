import uuid

from django.db import models

from events_app.models import Event


class Participant(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()
    confirmation_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    accepted_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    declined_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    is_confirmed = models.BooleanField(default=False, verbose_name='Email confirmed')
    invitation_sent = models.BooleanField(default=False)
    is_active = models.BooleanField(null=True, verbose_name='Invitation accepted')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.surname}'
