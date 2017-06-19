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

