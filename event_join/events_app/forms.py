from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import widgets, DateTimeInput, DateInput, ModelForm, CharField, DateTimeField

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
        widgets = {
            'start_date': DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}),
            'end_date': DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}),
            'registration_start': DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}),
            'registration_end': DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'})
        }

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


class SearchForm(forms.ModelForm):
    title = CharField(required=False)
    description = CharField(required=False)
    start_date = DateTimeField(required=False)

    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'start_date']


class UpdateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'start_date',
                  'end_date',
                  'registration_start',
                  'registration_end',
                  'limit',
                  'is_private']
