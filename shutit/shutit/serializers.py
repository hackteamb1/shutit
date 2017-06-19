from .models import Passenger as Passenger
from .models import _Queue as Queue
from rest_framework import serializers

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('passengers_count')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('user.first_name', 'user.last_name', 'is_in_queue', 'number_in_queue')
