from .models import Queue
from rest_framework import serializers

class QueueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Queue
        fields = ('url', 'passanger', 'is_waiting',
                  'boarding_time', 'arrival_time')
