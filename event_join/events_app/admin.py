from urllib.parse import urljoin

from django import forms
from django.core.mail import send_mail
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm

from events_app.models import Event
from event_join.settings import DOMAIN
from participants_app.models import Participant


def places_taken(obj):
    places = Participant.objects.filter(event=obj).count()
    return places


class InviteParticipantsForm(ActionForm):
    event = forms.ModelChoiceField(queryset=Event.objects.all())


def invite_participants(modeladmin, request, queryset):
    event = queryset.first()
    previous_event = request.POST.get('event')
    previous_event_obj = Event.objects.get(pk=previous_event)
    participants = Participant.objects.filter(event=previous_event)
    for p in participants:
        participant = Participant.objects.create(
            name=p.name,
            surname=p.surname,
            email=p.email,
            invitation_sent=True,
            event_id=event.pk
        )
        yes = urljoin(DOMAIN, f'participant/invite/{participant.accepted_id}')
        no = urljoin(DOMAIN, f'participant/invite/{participant.declined_id}')
        send_mail(
            f"{participant.name} - you've been invited to {previous_event_obj.title}",
            f'accept - {yes}; decline - {no}',
            'klosmartynaa@gmail.com',
            [participant.email],
        )


invite_participants.short_description = 'Send invitations to all who registered for'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "is_private", "limit", places_taken)
    verbose_name = "Event"
    verbose_name_plural = "Events"
    actions = [invite_participants]
    action_form = InviteParticipantsForm
    list_filter = [
        "title",
        "is_private",
        "start_date"
    ]
    search_fields = ("title", "description")
