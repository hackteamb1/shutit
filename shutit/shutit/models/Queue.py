from django.db import models


class Queue(models.Model):
    """Holds the queue of awaiting users."""
    passengers_count = models.IntegerField(default=0, null=False)

    class Meta:
        """Meta definition for Queue."""

        verbose_name = 'Queue'
        verbose_name_plural = 'Queues'

    def __str__(self):
        """Unicode representation of Queue."""
        return "%s - %s" % (self.arrival_time, self.passenger.user.username)

    def increment_passenger_count(self):
        self.passenger_copassengers_countunt += 1

    def get_passenger_count(self):
        return self.passengers_count

    def decrease_passenger_count(self):
        self.passengers_count -= 1

