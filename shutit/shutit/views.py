from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate


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