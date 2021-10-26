from django import forms
from django.core.exceptions import ValidationError

from events_app.models import Event
from .models import Participant


def validate_char(value):
    for i in value:
        if not i.isascii():
            raise ValidationError('Only letters and digits accepted!')


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=64, validators=[validate_char])
    surname = forms.CharField(max_length=64, validators=[validate_char])
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


