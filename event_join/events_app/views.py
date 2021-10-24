from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from .models import Event
from .forms import AddEventForm


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


class AddEventView(FormView):
    form_class = AddEventForm
    template_name = 'events_app/add_event.html'
    success_url = reverse_lazy('events-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)








