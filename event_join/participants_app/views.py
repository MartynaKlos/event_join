import uuid
from urllib.parse import urljoin

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import RegisterForm
from .models import Participant
from events_app.models import Event
from event_join.settings import DOMAIN


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        event_pk = kwargs['pk']
        event = get_object_or_404(Event, pk=event_pk)
        register_form = RegisterForm(initial={'event': event})
        context = {
            'form': register_form
        }
        if event.is_private:
            context['private'] = 'private'
        return render(request, 'participants_app/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            if event.count_places_left > 0:
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                email = form.cleaned_data['email']
                participant = Participant.objects.create(name=name, surname=surname, email=email, event=event)
                confirmation_uuid = f'participant/email/{participant.confirmation_id}'
                url = urljoin(DOMAIN, confirmation_uuid)
                send_mail(
                    f'{name} - Confirm your email',
                    f'Please confirm your email - {url}',
                    'klosmartynaa@gmail.com',
                    [email],
                )

                return render(request, 'participants_app/form_submitted.html')
            else:
                context = {
                    'form': form,
                    'message': 'Sorry, this event is full'
                }
                return render(request, 'participants_app/register.html', context)
        else:
            context = {
                'form': form
            }
            return render(request, 'participants_app/register.html', context)


class ConfirmEmailView(View):
    def get(self, request, *args, **kwargs):
        confirmation_id = kwargs['confirmation_uuid']
        participant = get_object_or_404(Participant, confirmation_id=confirmation_id)
        participant.is_confirmed = True
        participant.save()
        participant.confirmation_id = uuid.uuid1()
        participant.save()
        return render(request, 'participants_app/email_confirmed.html')


class AnswerInvite(View):
    def get(self, request, *args, **kwargs):
        answer_id = kwargs['answer_id']
        context = {}
        if Participant.objects.filter(accepted_id=answer_id):
            participant = get_object_or_404(Participant, accepted_id=answer_id)
            participant.is_active = True
            participant.is_confirmed = True
            participant.accepted_id = uuid.uuid1()
            participant.save()
            context['accepted'] = 'yes'
        else:
            participant = get_object_or_404(Participant, declined_id=answer_id)
            participant.is_active = False
            participant.is_confirmed = True
            participant.declined_id = uuid.uuid1()
            participant.save()
            context['accepted'] = 'no'
        return render(request, 'participants_app/accepted_invite.html', context)


