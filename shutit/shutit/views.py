from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from .serializers import QueueSerializer, StateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Queue, Passenger

def login(request):
    if request.POST:
        username = request.POST['id_number']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            ...
    if request.user.is_authenticated:
        redirect("index")
    return render(request, 'shutit/login.html')


class QueueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Queue.objects.filter(is_waiting=True).order_by('-id')
    serializer_class = QueueSerializer


@api_view(['GET'])
def passenger_state(request, passenger_id):
    try:
        passenger_state = Queue.objects.filter(
                        passenger=passenger_id, is_waiting=True).first()
    except ObjectDoesNotExist:
        content = {'message': 'You are not in the queue'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    serializer = StateSerializer(passenger_state, many=False, context={'request': request})
    return Response(serializer.data)


