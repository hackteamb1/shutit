from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import QueueSerializer, StateSerializer
from .models import _Queue as Queue
from .models import _Passenger as Passenger
import requests


CAPTCHA_SECRET = "6LfFJyYUAAAAAK5EDPeNa3kl84AqtCZjkju5znNS"


def index_view(request):
    if not request.user.is_authenticated():
        return redirect("login")

    if not request.user.is_staff:
        return render(request, 'shutit/index.html', context={'passenger': Passenger.objects.get(user=request.user)})
    else:
        return render(request, 'shutit/staff.html')


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

def validate_fields(first_name, last_name, id_number, email, password, password_verify):
    return None
    # TODO: This should return some error messages if the validation failes.

def validate_captcha(captcha):
    captcha_data = {"secret": CAPTCHA_SECRET, "response": captcha}
    res = requests.post("https://www.google.com/recaptcha/api/siteverify", captcha_data)
    return res.json()['success']



def signup_view(request):
    if request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        id_number = request.POST['id_number']
        email = request.POST['email']
        password = request.POST['password']
        password_verify = request.POST['password_verify']
        captcha = request.POST['g-recaptcha-response']
        errors = validate_fields(first_name, last_name, id_number, email, password, password_verify)
        errors = errors if errors else []
        if not validate_captcha(captcha) == True:
            errors.append("Captcha isn't verified.")

        if errors:
            return render(request, "shutit/signup.html", context={'errors': errors})
        try:
            hashed_id_number = Passenger.hash_id_number(id_number)
            user = User(username=hashed_id_number, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            passenger = Passenger(user=user, id_number=hashed_id_number)
            passenger.save()
        except Exception as e:
            try:
                user.delete()
                passenger.delete()
            except:
                # TODO : Make this better
                pass
            raise e
            # TODO : This should Exceot exceptions from the user and passenger creation. For example if idnum already exists



        login(request, user)
        return redirect("index")
    return render(request, "shutit/signup.html")


def signout_view(request):
    logout(request)
    return redirect("index")

@api_view(['GET'])
def passenger_state(request, passenger_id):
    """try:
        passenger = Passenger.objects.get(id_number=Passenger.hash_id_number(passenger_id))
    except Passenger.DoesNotExist:
        content = {'message': 'This user does not exist is the system'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
"""
    try:
        passenger = Passenger.objects.get(id_number=passenger_id)
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

@api_view(['POST'])
def remove_passenger_by_position(request):
    number_in_queue = request.data['number_in_queue']
    if not request.user.is_staff:
        content = {'message': 'You do not have permissions for that!'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    try:
        passenger = Passenger.objects.get(number_in_queue=number_in_queue)
    except Passenger.DoesNotExist:
        content = {'message': 'This user does not exist is the system'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    passenger.leave_queue()
    return redirect("index")

@api_view(['POST'])
def enter_passenger_by_id(request):
    passenger_id = request.data['passenger_id']
    if not request.user.is_staff:
        if not (Passenger.hash_id_number(passenger_id) == Passenger.objects.get(user=request.user).id_number):
            content = {'message': 'You do not have permissions for that!'}
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