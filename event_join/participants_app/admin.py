from urllib.parse import urljoin

from django import forms
from django.core.mail import send_mail
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm

from events_app.models import Event
from event_join.settings import DOMAIN
from participants_app.models import Participant


def full_name(obj):
    return f"{obj.name} {obj.surname}"


def send_invitation(modeladmin, request, queryset):
    event_id = request.POST.get('event')
    event = Event.objects.get(pk=event_id)
    for obj in queryset:
        if obj.event_id != event_id:
            participant = Participant.objects.create(
                name=obj.name,
                surname=obj.surname,
                email=obj.email,
                invitation_sent=True,
                event_id=event_id,
            )
            yes = urljoin(DOMAIN, f'participant/invite/{participant.accepted_id}')
            no = urljoin(DOMAIN, f'participant/invite/{participant.declined_id}')
            send_mail(
                f"{participant.name} - you've been invited to {event.title}",
                f'accept - {yes}; decline - {no}',
                'klosmartynaa@gmail.com',
                [participant.email],
            )


send_invitation.short_description = 'Send invitations to participants'


class SendInviteForm(ActionForm):
    event = forms.ModelChoiceField(queryset=Event.objects.filter(is_private=True))


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (full_name, "email", "is_confirmed", "invitation_sent", "is_active", "event")
    verbose_name = "Participant"
    verbose_name_plural = "Participants"
    actions = [send_invitation]
    action_form = SendInviteForm
    list_filter = [
        "event",
        "invitation_sent",
        "is_confirmed",
        "is_active"
    ]
    search_fields = ("name", "surname", "email")
