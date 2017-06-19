from django.db import models
from django.contrib.auth.models import User

class Passenger(models.Model):
    """
    Represents a passenger, an extension for the User model.
    """

    user = models.OneToOneField(to=User, null=False)
    id_number = models.TextField(max_length=65, null=False)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

