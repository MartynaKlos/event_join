from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Permission
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, FormView, RedirectView, UpdateView

from rest_framework import viewsets

from .forms import AddEventForm, LoginForm, SearchForm, UpdateEventForm, AddUserForm
from .models import Event
from events_api.serializers import EventSerializer


def error_404_view(request, exception):
    context = {}
    template = loader.get_template('events_app/errors/404.html')
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
        queryset = Event.objects.filter(is_private=False, start_date__gte=timezone.now())
        return queryset


class UserOnlyEventsListView(ListView):
    context_object_name = 'events'
    template_name = 'events_app/events_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.filter(is_private=False, start_date__gte=timezone.now(), user=self.request.user)
        return queryset


class EventDetailsView(DetailView):
    model = Event
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'
    template_name = 'events_app/event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['places_left'] = context['object'].count_places_left
        context['available'] = context['object'].available
        return context


class AddEventView(PermissionRequiredMixin, FormView):
    form_class = AddEventForm
    template_name = 'events_app/add_event.html'
    success_url = reverse_lazy('events-list')
    permission_required = 'events_app.add_event'

    def form_valid(self, form):
        event = form.save()
        event.user = self.request.user
        event.save()
        return super().form_valid(form)


class AddUserView(FormView):
    template_name = 'events_app/add_user.html'
    form_class = AddUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        cd = form.cleaned_data
        user = User.objects.create_user(
            username=cd['username'],
            password=cd['password1'],
            email=cd['email']
        )
        permission_add = Permission.objects.get(codename='add_event')
        permission_change = Permission.objects.get(codename='change_event')
        user.user_permissions.add(permission_add, permission_change)
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
    success_url = reverse_lazy('events-list')

    def form_valid(self, form):
        cd = form.cleaned_data
        context = {
            'form': form
        }
        events = Event.objects.filter(is_private=False)
        if cd['title']:
            events = events.filter(title__icontains=cd['title'])
        if cd['description']:
            events = events.filter(description__icontains=cd['description'])
        if cd['start_date']:
            events = events.filter(start_date__gte=cd['start_date'])
        index = 1
        for event in events:
            event.index = index
            index += 1
        context['events'] = events
        if events.count() == 0:
            context['message'] = "No events matched your search..."
        return render(self.request, 'events_app/search_event.html', context)


class UpdateEventView(PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = UpdateEventForm
    template_name = 'events_app/update_event.html'
    pk_url_kwarg = 'event_pk'
    success_url = reverse_lazy('events-list')
    permission_required = 'events_app.change_event'

    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['event_pk'], user=self.request.user)
        form = self.form_class(initial={
            'title': event.title,
            'description': event.description,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'registration_start': event.registration_start,
            'registration_end': event.registration_end,
            'limit': event.limit,
            'is_private': event.is_private
        })
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

