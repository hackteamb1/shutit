from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from rest_framework import viewsets
from .serializers import QueueSerializer
from .models import _Queue as Queue

def index_view(request):
    if request.user.is_authenticated():
        return render(request, 'shutit/index.html')
    return redirect("login")

def login_view(request):
    if request.POST:
        id_number = request.POST['id_number']
        password = request.POST['password']
        user = authenticate(request, id_number=id_number, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            return render(request, 'shutit/login.html', context={'wrong': True})

    if request.user.is_authenticated():
        return redirect("index")

    return render(request, 'shutit/login.html')

def signup_view(request):
    return render("shutit/signup.html")

def signout_view(request):
    logout(request)
    return redirect("index")


class QueueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Queue.objects.filter(is_waiting=True)
    serializer_class = QueueSerializer
