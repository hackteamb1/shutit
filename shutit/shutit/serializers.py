from .models import _Passenger as Passenger
from .models import _Queue as Queue
from rest_framework import serializers

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('passengers_count')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('first_name', 'last_name', 'number_in_queue')
