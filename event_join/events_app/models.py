from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    limit = models.IntegerField()
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def available(self):
        if self.registration_start <= timezone.now():
            self.available = True
        else:
            self.available = False
        return self.available

