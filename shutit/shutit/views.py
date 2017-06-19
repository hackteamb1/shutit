from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
from .serializers import QueueSerializer

from .models import Queue

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
    queryset = Queue.objects.filter(is_waiting=True)
    serializer_class = QueueSerializer

