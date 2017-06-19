from django.db import models
from . import Passenger


class Queue(models.Model):
    """Holds the queue of awaiting users."""

    arrival_time = models.DateTimeField()
    boarding_time = models.DateTimeField(blank=True)
    is_waiting = models.BooleanField(default=True)
    passanger = models.ForeignKey(Passenger)

    class Meta:
        """Meta definition for Queue."""

        verbose_name = 'Queue'
        verbose_name_plural = 'Queues'

    def __unicode__(self):
        """Unicode representation of Queue."""
        pass
