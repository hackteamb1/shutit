from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import QueueSerializer, StateSerializer
from .models import _Queue as Queue
from .models import _Passenger as Passenger

def index_view(request):
    if request.user.is_authenticated():
        return render(request, 'shutit/index.html')
    return redirect("login")

def login_view(request):
    if request.POST:
        id_number = request.POST['id_number']
        password = request.POST['password']
        hashed_id_number = Passenger.hash_id_number(id_number)
        user = authenticate(request, id_number=hashed_id_number, password=password)
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
        passenger = Passenger.objects.get(id_number=Passenger.hash_id_number(passenger_id))
    except Passenger.DoesNotExist:
        content = {'message': 'This user does not exist is the system'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    serializer = StateSerializer(passenger, many=False, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def queue_state(request, amount_of_top_users):
    try:
        passengers = Passenger.objects.exclude(number_in_queue=None).order_by('number_in_queue')[:int(amount_of_top_users)]
    except Passenger.DoesNotExist:
        content = {'message': 'No passengers?'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    serializer = StateSerializer(passengers, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['DELETE'])
def remove_passenger_by_id(request):
    import pdb; pdb.set_trace()
    passenger_id = request.data['passenger_id']
    if (not Passenger.hash_id_number(passenger_id) == Passenger.objects.get(user=request.user).id_number) and not request.user.is_staff: #TODO: add prem to ktsinto.
        content = {'message' : 'You do not have permissions for that!'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    print("YES! you are auth")
    try:
        passenger = Passenger.objects.get(id_number=Passenger.hash_id_number(passenger_id))
    except Passenger.DoesNotExist:
        content = {'message': 'This user does not exist is the system'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    passenger.leave_queue()
    return redirect("index")

@api_view(['POST'])
def enter_passenger_by_id(request):
    import pdb;pdb.set_trace()
    passenger_id = request.data['passenger_id']
    if not request.user.is_staff:
        if not (Passenger.hash_id_number(passenger_id) == Passenger.objects.get(user=request.user).id_number):
            content = {'message': 'You do not have permissions for thact!'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    try:
        passenger = Passenger.objects.get(id_number=Passenger.hash_id_number(passenger_id))
    except Passenger.DoesNotExist:
        content = {'message': 'This user does not exist is the system'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    queue = Queue.objects.all()[0]
    passenger.enter_queue(queue)
    return redirect('index')

class QueueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer