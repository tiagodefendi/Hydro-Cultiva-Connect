from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from myapp.models import Property, Devices

import re
COORD_PATTERN = r'^-?[\d]+\.[\d]+$'
KEY_PATTERN = r'^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$'

def add_device(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        name = request.POST.get('name')
        key = request.POST.get('key')

        print(f'{name}: {type} = {key}')
    return render(request, 'add_device.html')

@login_required(login_url='login')
def add_property(request):
    if request.method == 'POST':
        name: str = request.POST.get('name')
        description: str = request.POST.get('description')
        latitude: str = request.POST.get('latitude')
        longitude: str = request.POST.get('longitude')

        print(f'{name} C({latitude}, {longitude}) - {description}')

        if re.match(KEY_PATTERN, latitude):
            latitude: float = float(latitude)
        else:
            return render(request, {'error': 'Invalid latitude coordinate'})
        if re.match(KEY_PATTERN, longitude):
            longitude: float = float(longitude)
        else:
            return render(request, {'error': 'Invalid longitude coordinate'})

        try:
            property = Property(
                name=name,
                description=description,
                latitude=latitude,
                longitude=longitude,
                user=request.user  # authenticated user
            )

            property.save()
        except:
            return render(request, {'error': 'Something wrong happening'})


    return render(request, 'add_property.html')

@login_required(login_url='login')
def properties(request):
    return render(request, 'properties.html')

@login_required(login_url='login')
def logout(request):
    auth_logout(request) #desloga o usuário

    return redirect('login')

# General/No login required --------------------------------------------------------------

def login(request):
    if request.method == 'POST':
        username: str = request.POST.get('username')
        password: str = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('home')
        except:
            return render(request, 'login.html', {'error': 'Username or password wrong'})


    return render(request, 'login.html')

#TODO: verify SQL injections
def signup(request):
    if request.method == 'POST': #getting forms information
        first_name: str = request.POST.get('first_name')
        last_name: str = request.POST.get('last_name')
        username: str = request.POST.get('username')
        email: str = request.POST.get('email')
        password: str = request.POST.get('password')
        confirm_password: str = request.POST.get('confirm_password')

        print(f"{first_name} {last_name} - {username}: {email} - {password}") # log request signup on terminal

        if password == confirm_password: # verify if password is equal confirm_password and continue
            if User.objects.filter(username=username).exists(): # verify if this username is already in use
                    return render(request, 'signup.html', {'error': 'Username already in use'})

            if User.objects.filter(email=email).exists(): # verify if this email is already in use
                    return render(request, 'signup.html', {'error': 'E-mail already in useo'})

            try:
                user:User = User.objects.create_user( # create user object
                    first_name = first_name,
                    last_name= last_name,
                    username=username,
                    email=email,
                    password=password
                    )

                user.save() # insert new user in database

                return redirect('login') # go to login page
            except Exception as e:
                return render(request, 'signup.html', {'error': f'{e}'}) # up error in page
        else:
            return render(request, 'signup.html', {'error': 'Passwords don\'t match'}) # password don't match


    return render(request, 'signup.html')

def home(request):


    return render(request, 'index.html')
