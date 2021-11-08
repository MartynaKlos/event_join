from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render
from django.template import context, Engine
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, RedirectView

from rest_framework import viewsets

from .forms import AddEventForm, LoginForm, SearchForm
from .models import Event
from events_api.serializers import EventSerializer


def error_404_view(request, exception):
    template = Engine().from_string('events_app/errors/404.html')
    body = template.render(context, request)
    content_type = None
    return HttpResponseNotFound(body, content_type=content_type)


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class Main(View):
    def get(self, request):
        return render(request, 'events_app/main.html')


class EventsListView(ListView):
    context_object_name = 'events'
    template_name = 'events_app/events_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.filter(is_private=False)
        index = 1
        for event in queryset:
            event.index = index
            index += 1
        return queryset


class EventDetailsView(DetailView):
    model = Event
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'
    template_name = 'events_app/event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_pk = context['object'].pk
        context['places_left'] = context['object'].count_places_left
        context['available'] = context['object'].available
        return context


class AddEventView(PermissionRequiredMixin, FormView):
    form_class = AddEventForm
    template_name = 'events_app/add_event.html'
    success_url = reverse_lazy('events-list')
    permission_required = 'events_app.add_event'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'events_app/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, form.user)
        return response


class LogoutView(RedirectView):
    url = reverse_lazy('main')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, *kwargs)


class SearchEventView(FormView):
    template_name = 'events_app/search_event.html'
    form_class = SearchForm

    def post(self, request, *args, **kwargs):
        form = self.get_form(form_class=SearchForm)
        if form.is_valid():
            pass
        else:
            pass


class TestError(View):
    def get(self, request):
        raise Http404
