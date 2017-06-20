from django.db import models
from django.contrib.auth.models import User
from .Queue import Queue

from hashlib import sha256

class Passenger(models.Model):
    """
    Represents a passenger, an extension for the User model.
    """

    user = models.OneToOneField(to=User, null=False)
    id_number = models.TextField(max_length=65, null=False, unique=True, primary_key=True)
    queue = models.ForeignKey(to=Queue, null=True, blank=True)
    number_in_queue = models.IntegerField(null=True, blank=True, editable=True)#False)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def delete(self, *args, **kwargs):
        if self.queue:
            self.queue.decrease_passenger_count()
        super(Passenger, self).delete(*args, **kwargs)

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def enter_queue(self, queue):
        self.queue = queue
        self.queue.increment_passenger_count()
        self.number_in_queue = self.queue.passengers_count
        self.save()

    def leave_queue(self):
        self.update_passenger_positions(self.number_in_queue)
        self.queue.decrease_passenger_count()
        self.queue = None
        self.number_in_queue = None
        self.save()

    def get_queue_placement(self):
        return self.number_in_queue

    def update_passenger_positions(self, lowest_position):
        for passenger in Passenger.objects.filter(queue=self.queue):
            if passenger.number_in_queue > lowest_position:
                passenger.number_in_queue -= 1
                passenger.save()

    @staticmethod
    def hash_id_number(id_number):
        return sha256(id_number.encode('utf-8')).hexdigest()