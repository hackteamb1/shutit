from django.db import models


class Queue(models.Model):
    """Holds the queue of awaiting users."""
    name = models.TextField(max_length=20, null=False)
    passengers_count = models.IntegerField(default=0, null=False)

    class Meta:
        """Meta definition for Queue."""

        verbose_name = 'Queue'
        verbose_name_plural = 'Queues'

    def increment_passenger_count(self):
        self.passengers_count += 1

    def get_passenger_count(self):
        return self.passengers_count

    def decrease_passenger_count(self):
        self.passengers_count -= 1

