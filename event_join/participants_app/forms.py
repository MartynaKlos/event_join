from django import forms

from events_app.models import Event
from .models import Participant


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=64)
    surname = forms.CharField(max_length=64)
    email = forms.EmailField()
    event = forms.ModelChoiceField(queryset=Event.objects.filter(is_private=False))

    # def clean(self):
    #     cd = super().clean()
    #     name = cd['name']
    #     surname = cd['surname']
    #     email = cd['email']
    #     event = cd['event']
    #     Participant.objects.create(name=name,
    #                                surname=surname,
    #                                email=email,
    #                                event=event)


