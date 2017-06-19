from django.db import models


class Queue(models.Model):
    """Holds the queue of awaiting users."""

    time_added = models.DateTimeField()
    

    class Meta:
        """Meta definition for Queue."""

        verbose_name = 'Queue'
        verbose_name_plural = 'Queues'

    def __unicode__(self):
        """Unicode representation of Queue."""
        pass
