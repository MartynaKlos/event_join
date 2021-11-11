from rest_framework import serializers

from events_app.models import Event
from participants_app.models import Participant


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'start_date',
                  'end_date',
                  'registration_start',
                  'registration_end',
                  'is_private',
                  'limit',
                  'id']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['name',
                  'surname',
                  'email',
                  'is_confirmed',
                  'invitation_sent',
                  'is_active',
                  'event']