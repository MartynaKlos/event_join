from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import widgets, DateTimeInput, CharField, DateTimeField

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


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    password1 = forms.CharField(min_length=10, widget=widgets.PasswordInput)
    password2 = forms.CharField(min_length=10, widget=widgets.PasswordInput)

    def clean_login(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken!')
        return username

    def clean(self):
        cd = super().clean()
        password1 = cd['password1']
        password2 = cd['password2']
        if password2 != password1:
            raise ValidationError('Passwords are not identical!')
