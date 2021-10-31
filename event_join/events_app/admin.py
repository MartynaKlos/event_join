from django.contrib import admin

from events_app.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "is_private")
    verbose_name = "Event"
    verbose_name_plural = "Events"
