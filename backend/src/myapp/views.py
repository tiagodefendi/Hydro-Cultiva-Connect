from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from myapp.models import Property, Devices
from django.http import HttpResponse
from django.template import loader
import json

# Regex -------------------------------------------------------------------------------------------------------
import re
COORD_PATTERN = r'^-?[\d]+\.[\d]+$'
KEY_PATTERN = r'^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$'

# Views ------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def add_device(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        name = request.POST.get('name')
        key = request.POST.get('key')

        print(f'{name}: {type} = {key}')
    return render(request, 'add_device.html')

# Properties ->
@login_required(login_url='login')
def property(request, id: int):
    property: Property = get_object_or_404(Property, id= id)

    if property.user != request.user: # verify if this user has property
        return redirect('properties')

    return render(request, 'property.html', {'property': property})

@login_required(login_url='login')
def properties(request):
    properties = Property.objects.filter(user=request.user)
    properties_data = [
        {
            'latitude': property.latitude,
            'longitude': property.longitude,
            'id': property.id,
            'name': property.name,
            'description': property.description
        }
        for property in properties
    ]
    properties_json = json.dumps(properties_data)
    template = loader.get_template('properties.html')
    context = {'properties_json': properties_json}
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def add_property(request):
    if request.method == 'POST':
        name: str = request.POST.get('name')
        description: str = request.POST.get('description')
        latitude: str = request.POST.get('latitude')
        longitude: str = request.POST.get('longitude')

        print(f'{name} C({latitude}, {longitude}) - {description}')

        if re.match(COORD_PATTERN, latitude):
            latitude: float = float(latitude)
        else:
            return render(request, 'add_property.html', {'error': 'Invalid latitude coordinate'})
        if re.match(COORD_PATTERN, longitude):
            longitude: float = float(longitude)
        else:
            return render(request, 'add_property.html', {'error': 'Invalid longitude coordinate'})

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
            return render(request, 'add_property.html', {'error': 'Something wrong happened'})


    return render(request, 'add_property.html')

# User ->
@login_required(login_url='login')
def profile(request, username: str):
    user: User = get_object_or_404(User, username= username)

    return render(request, 'profile.html', {'user': user})

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
            else:
                return render(request, 'login.html', {'error': 'User is not registered'})
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
    if request.user.is_authenticated:
        return render(request, 'index.html', {'username': request.user.username})
    else:
        return render(request, 'index-nl.html')
