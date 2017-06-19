from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
from .serializers import QueueSerializer
from .models import _Queue as Queue

def index_view(request):
    return render(request, 'shutit/index.html')

def login_view(request):
    if request.POST:
        id_number = request.POST['id_number']
        password = request.POST['password']
        passenger = authenticate(request, id_number=id_number, password=password)
        if passenger:
            login(request, passenger)
            redirect("index")
        else:
            return render(request, 'shutit/login.html', context={'wrong': True})

    if request.user.is_authenticated:
        redirect("index")

    return render(request, 'shutit/login.html')

def signup_view(request):
    pass


class QueueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Queue.objects.filter(is_waiting=True)
    serializer_class = QueueSerializer
