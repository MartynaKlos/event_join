from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import Event


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'limit',
                  'start_date',
                  'end_date',
                  'registration_start',
                  'registration_end',
                  'is_private']


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        username = cd['username']
        password = cd['password']
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError('Incorrect username or password!')