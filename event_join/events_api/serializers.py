from rest_framework import serializers

from events_app.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'id']
