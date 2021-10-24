from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.core.mail import send_mail

from .forms import RegisterForm
from .models import Participant
from events_app.models import Event


# class RegisterView(FormView):
#     form_class = RegisterForm
#     template_name = 'participants_app/register.html'
#     success_url = reverse_lazy('events-list')
#
#     def form_valid(self, form):
#         send_mail(
#             'Confirm your email',
#             'Please confirm your email',
#             'klosmartynaa@gmail.com',
#             ['klos.martyna@wp.pl'],
#         )
#         return super().form_valid(form)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        event_pk = int(request.GET.get('event'))
        event = Event.objects.get(pk=event_pk)
        register_form = RegisterForm(initial={'event': event})
        context = {
            'form': register_form
        }
        return render(request, 'participants_app/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            event = form.cleaned_data['event']
            Participant.objects.create(name=name, surname=surname, email=email, event=event)
            confirmation_uuid = Participant.objects.get(email=email).confirmation_id
            url = f'http://127.0.0.1:8000/participant/{confirmation_uuid}'

            send_mail(
                f'{name} - Confirm your email',
                f'Please confirm your email - {url}',
                'klosmartynaa@gmail.com',
                [email],
            )

            return render(request, 'participants_app/form_submitted.html')


class ConfirmEmailView(View):
    def get(self, request, *args, **kwargs):
        confirmation_id = kwargs['confirmation_uuid']
        participant = Participant.objects.get(confirmation_id=confirmation_id)
        participant.is_confirmed = True
        participant.save()
        return render(request, 'participants_app/email_confirmed.html')

