from .models import Queue
from rest_framework import serializers

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('passenger', 'is_waiting',
                  'boarding_time', 'arrival_time')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('passenger', 'is_waiting',
                  'boarding_time', 'arrival_time')
