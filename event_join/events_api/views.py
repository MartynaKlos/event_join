from rest_framework import viewsets, permissions

from events_app.models import Event
from participants_app.models import Participant
from .serializers import EventSerializer, ParticipantSerializer


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ParticipantsViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
