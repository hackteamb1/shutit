from django.contrib.auth.models import User
from .models import _Passenger as Passenger


class IDBackend(object):
    """
    Authenticate against the ID Number of a passenger and the user's password.
    """

    def authenticate(self, request, id_number, password):
        try:
            passenger = Passenger.objects.get(id_number=id_number)
            pwd_valid = passenger.user.check_password(password)

        except Passenger.DoesNotExist:
            return None

        if not pwd_valid:
            return None

        return passenger.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None