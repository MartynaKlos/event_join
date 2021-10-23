from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from .models import Event


class Main(View):
    def get(self, request):
        return render(request, 'events_app/main.html')


class EventsListView(ListView):
    context_object_name = 'events'
    template_name = 'events_app/events_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.filter(is_private=False)
        return queryset


class EventDetailsView(DetailView):
    model = Event
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'
    template_name = 'events_app/event_details.html'





