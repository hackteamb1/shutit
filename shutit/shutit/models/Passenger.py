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
    is_in_queue = models.BooleanField()
    number_in_queue = models.IntegerField(default=0, null=True)
    queue = models.ForeignKey(to=Queue, null=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def enter_queue(self, queue):
        self.queue = queue
        self.queue.increment_passenger_count()
        self.number_in_queue = self.queue.get_passenger_count()
        self.is_in_queue = True

    def leave_queue(self):
        self.queue.update_passenger_positions(self.number_in_queue)
        self.update_passenger_positions(self.number_in_queue, self.queue)
        self.queue.decrease_passenger_count()
        self.is_in_queue = False
    
    def get_queue_placement(self):
        return self.number_in_queue

    def update_passenger_positions(self, lowest_position):
        for passenger in Passenger.objects.filter(queue=self.queue):
            if passenger.number_in_queue > lowest_position:
                passenger.number_in_queue -= 1

    @staticmethod
    def hash_id_number(id_number):
        m = sha256()
        m.update(id_number)
        return m.digest()
