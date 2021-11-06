from django import forms
from django.contrib.auth import authenticate
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.forms import Textarea, DateTimeInput
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

    # def __init__(self, *args, **kwargs):
    #     super(AddEventForm, self).__init__(self, *args, **kwargs)
    #     self.fields['start_date'].widget = widgets.AdminSplitDateTime()


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


class SearchForm(forms.Form):
    title = forms.CharField(label='event', max_length=100, widget=forms.TextInput),
    description = forms.CharField(label='description', widget=forms.Textarea),
    start_date = forms.DateTimeField(label='Start date', widget=forms.DateTimeInput)
