from django.contrib.auth.models import User
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
    is_private = models.BooleanField(default=False, verbose_name='Private')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    @property
    def available(self):
        if self.registration_start <= timezone.now():
            return True
        else:
            return False

    @property
    def count_places_left(self):
        return self.limit - self.participant_set.filter(event=self.pk).count()

