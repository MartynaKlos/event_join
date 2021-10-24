from django import forms

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
