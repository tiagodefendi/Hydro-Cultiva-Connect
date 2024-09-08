from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from myapp.models import Property, Device
from django.http import HttpResponse
from django.template import loader
import json
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

# Regex -------------------------------------------------------------------------------------------------------
import re

# coordinates
COORD_PATTERN = r'^-?[\d]+\.[\d]+$'

# device's key
KEY_PATTERN = r'^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$'

# username
USERNAME_PATTERN = r'^(?!_)[a-z0-9_]{3,20}(?<!_)$'
'''
Usernames only accepted
- 3 to 20 characters
- lowercase letters
- numbers from 0 to 9
- and underscore "_"
'''

# email
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
'''
address@domain.topleveldomain
'''

# password
PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'
'''
Password Requirements:
- At least 6 characters long
- Includes at least one lowercase letter (a-z)
- Includes at least one uppercase letter (A-Z)
- Includes at least one digit (0-9)
- *Includes at least one special character (e.g., @, $, !, %, , ?, &)
'''

# Views ------------------------------------------------------------------------------------------------------

# Device ->

@login_required(login_url='login')
def device_live(request, property_id: int, device_id: int, link: str):
    property: Property = get_object_or_404(Property, id= property_id)
    user: User = property.user
    device: Device = get_object_or_404(Device, id=device_id)

    if user != request.user: # verify if this user has property
        return redirect('properties')

    if device.type != 'Camera':
        return redirect('properties')

    return render(request, 'device_live.html', {'property': property, 'device': device, 'link':link})

@login_required(login_url='login')
def delete_device(request, property_id: int, device_id: int):
    property: Property = get_object_or_404(Property, id= property_id)
    user: User = property.user
    device: Device = get_object_or_404(Device, id=device_id)

    if user != request.user: # verify if this user has property
        return redirect('properties')

    if request.method == 'POST':
        user = request.user
        device.delete()
        return redirect('properties')

    return render(request, 'delete_device.html', {'property': property, 'device': device})

#------------------------------------

@login_required(login_url='login')
def edit_device(request, property_id: int, device_id: int):
    property: Property = get_object_or_404(Property, id= property_id)
    user: User = property.user
    device: Device = get_object_or_404(Device, id=device_id)

    if user != request.user: # verify if this user has property
        return redirect('properties')

    if request.method == 'POST':
        new_type = request.POST.get('type')
        new_name = request.POST.get('name')
        new_key = request.POST.get('key')

        try:
            if new_type and new_type != device.type:
                device.type = new_type.strip()

            if new_name and new_name != device.name:
                device.name = new_name.strip()

            if new_key and new_key != device.key:
                device.key = new_key.strip()

            device.save()

            return redirect(f'properties')

        except Exception as e:
            return render(request, 'edit_device.html', {'property': property, 'device': device, 'error': 'Something went wrong'})

    return render(request, 'edit_device.html', {'property': property, 'device': device})

#------------------------------------

@login_required(login_url='login')
def device(request, property_id: int, device_id: int):
    property: Property = get_object_or_404(Property, id= property_id)

    if property.user != request.user: # verify if this user has property
        return redirect('properties')

    device: Device = get_object_or_404(Device, id=device_id)

    return render(request, 'device.html', {'property': property, 'device': device})

#------------------------------------

@login_required(login_url='login')
def add_device(request, id: int):
    property = get_object_or_404(Property, id=id)

    if request.method == 'POST':
        type: str = request.POST.get('type').strip()
        name: str = request.POST.get('name').strip()
        key: str = request.POST.get('key').strip()

        if not re.fullmatch(KEY_PATTERN, key):
            return render(request, 'add_device.html', {'id':property.id, 'error': 'Invalid key code'})

        device: Device = Device(
            type=type,
            name=name,
            key=key,
            property=property
        )
        device.save()
        return redirect(f'/properties/{property.id}')

    return render(request, 'add_device.html', {'id':property.id})

#------------------------------------

# Properties ->
@login_required(login_url='login')
def delete_property(request, property_id: int):
    property: Property = get_object_or_404(Property, id= property_id)
    user: User = property.user

    if user != request.user: # verify if this user has property
        return redirect('properties')

    if request.method == 'POST':
        user = request.user
        property.delete()
        return redirect('properties')

    return render(request, 'delete_property.html', {'property': property})

#------------------------------------

def edit_property(request, property_id: int):
    property: Property = get_object_or_404(Property, id= property_id)

    if property.user != request.user: # verify if this user has property
        return redirect('properties')

    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_description = request.POST.get('description')
        new_latitude = request.POST.get('latitude')
        new_longitude = request.POST.get('longitude')

        try:
            if new_name and new_name != property.name:
                property.name = new_name.strip()

            if new_description != property.description:
                property.description = new_description

            if new_latitude and new_latitude != property.latitude:
                if re.fullmatch(COORD_PATTERN, new_latitude.strip()):
                    new_latitude: float = float(new_latitude.strip())
                else:
                    return render(request, 'edit_property.html', {'error': 'Invalid latitude coordinate'})

                property.latitude = new_latitude

            if new_longitude and new_longitude != property.longitude:
                if re.fullmatch(COORD_PATTERN, new_longitude.strip()):
                    new_longitude: float = float(new_longitude.strip())
                else:
                    return render(request, 'edit_property.html', {'error': 'Invalid longitude coordinate'})

                property.longitude = new_longitude

            property.save()

            return redirect('properties')

        except Exception as e:
            return render(request, 'edit_property.html', {'property': property, 'error': 'Something went wrong'})

    return render(request, 'edit_property.html', {'property': property})

#------------------------------------

@login_required(login_url='login')
def property(request, property_id: int):
    property: Property = get_object_or_404(Property, id= property_id)

    if property.user != request.user: # verify if this user has property
        return redirect('properties')

    devices: list[Device] = Device.objects.filter(property=property)

    return render(request, 'property.html', {'property': property, 'devices': devices})

#------------------------------------

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

#------------------------------------

@login_required(login_url='login')
def add_property(request):
    if request.method == 'POST':
        name: str = request.POST.get('name').strip()
        description: str = request.POST.get('description').strip()
        latitude: str = request.POST.get('latitude').strip()
        longitude: str = request.POST.get('longitude').strip()

        print(f'{name} C({latitude}, {longitude}) - {description}')

        if re.fullmatch(COORD_PATTERN, latitude):
            latitude: float = float(latitude)
        else:
            return render(request, 'add_property.html', {'error': 'Invalid latitude coordinate'})
        if re.fullmatch(COORD_PATTERN, longitude):
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
            return redirect('properties')
        except:
            return render(request, 'add_property.html', {'error': 'Something wrong happened'})


    return render(request, 'add_property.html')

# User ->
@login_required(login_url='login')
def edit_profile(request, username: str):
    try:
        user: User = get_object_or_404(User, username=username)
    except:
        return redirect('edit_profile', username=request.user.username)

    if request.user != user:
        return redirect('edit_profile', username=request.user.username)

    if request.method == 'POST':
        new_first_name: str = request.POST.get('first_name')
        new_last_name: str = request.POST.get('last_name')
        new_username: str = request.POST.get('username')
        new_email: str = request.POST.get('email')

        try:
            #saving new information
            if new_first_name and new_first_name != user.first_name:
                user.first_name = new_first_name.strip()

            if new_last_name and new_last_name != user.last_name:
                user.last_name = new_last_name.strip()

            if new_username and new_username != user.username:
                if not re.fullmatch(USERNAME_PATTERN, new_username):
                    return render(request, 'edit_profile.html', {'user': user, 'error': f'Invalid username'})

                if User.objects.filter(username=new_username.strip()).exists(): # verify if this username is already in use
                    return render(request, 'edit_profile.html', {'user': user, 'error': 'Username already in use'})
                user.username = new_username.strip()

            if new_email and new_email != user.email:
                if not re.fullmatch(EMAIL_PATTERN, new_email):
                    return render(request, 'edit_profile.html', {'user': user, 'error': f'Invalid email'})
                if User.objects.filter(email=new_email.strip()).exists(): # verify if this email is already in use
                    return render(request, 'edit_profile.html', {'user': user, 'error': 'E-mail already in use'})
                user.email = new_email.strip()

            user.save()

            return redirect('profile', username=user.username)
        except:
            return render(request, 'edit_profile.html', {'user': user, 'error': 'Something wrong happened'})

    return render(request, 'edit_profile.html', {'user': user})

#------------------------------------

#TODO: change password
@login_required(login_url='login')
def change_password(request, username:str):
    try:
        user: User = get_object_or_404(User, username=username)
    except:
        return redirect('change_password', username=request.user.username)

    if (request.user != user):
        return redirect('change_password', username=request.user.username)
    
    if request.method == 'POST':
        old_password: str = request.POST.get('old_password')
        new_password: str = request.POST.get('new_password')
        confirm_new_password: str = request.POST.get('confirm_new_password')

        if not user.check_password(old_password):
            return render(request, 'change_password.html', {'user': user, 'error': 'Incorrect current password'})
        
        if not re.fullmatch(PASSWORD_PATTERN, new_password):
                return render(request, 'change_password.html', {'error': 'Invalid password'})
        
        if user.check_password(new_password):
            return render(request, 'change_password.html', {'user': user, 'error': 'Use another password'})

        if new_password != confirm_new_password:
            return render(request, 'change_password.html', {'user': user, 'error': 'Passwords do not match'})
        
        user.set_password(new_password)
        user.save()
        return redirect('login')

    return render(request, 'change_password.html', {'user': user})

#------------------------------------

@login_required(login_url='login')
def delete_account(request, username: str):
    try:
        user: User = get_object_or_404(User, username=username)
    except:
        return redirect('profile', username=request.user.username)

    if request.user != user:
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')

    return render(request, 'delete_account.html', {'user': user})

#------------------------------------

@login_required(login_url='login')
def profile(request, username: str):
    try:
        user: User = get_object_or_404(User, username=username)
    except:
        return redirect('profile', username=request.user.username)

    if request.user != user:
        return redirect('profile', username=request.user.username)

    return render(request, 'profile.html', {'user': user})

#------------------------------------

@login_required(login_url='login')
def logout(request):
    auth_logout(request) #desloga o usuário

    return redirect('home')

# General/No login required --------------------------------------------------------------

#TODO: recover password
def password_reset_invalid(request):
    return render(request, 'password_reset_invalid.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_new_password')

            if new_password and confirm_password:
                if not re.fullmatch(PASSWORD_PATTERN, new_password):
                    return render(request, 'password_reset_confirm.html', {'error': f'Invalid password', 'uid': uidb64, 'token': token})

                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    
                    return redirect('password_reset_complete')
                else:
                    return render(request, 'password_reset_confirm.html', {'error': 'Passwords don\'t match', 'uid': uidb64, 'token': token})
            else:
                return render(request, 'password_reset_confirm.html', {'error': 'Both password fields are required', 'uid': uidb64, 'token': token})

        return render(request, 'password_reset_confirm.html', {'uid': uidb64, 'token': token})
    else:
        return redirect('password_reset_invalid')

def password_reset_request(request):
    if request.method == 'POST':
        user_verify: str = request.POST.get('user_verify').strip()

        if re.fullmatch(USERNAME_PATTERN, user_verify):
            user = User.objects.filter(username=user_verify).first()
        elif re.fullmatch(EMAIL_PATTERN, user_verify):
            user = User.objects.filter(email=user_verify).first()
        else:
            return render(request, 'password_reset_request.html', {'error': f'Invalid username or email'})

        if user:
            subject = "Password Reset Requested"
            email_template_name = "password_reset_email.html"
            context = {
                "email": user.email,
                'domain': get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
                'protocol': 'http',
            }
            email_body = render_to_string(email_template_name, context)
            send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

            return redirect('password_reset_done')
    
    return render(request, "password_reset_request.html")

#------------------------------------

def login(request):
    if request.method == 'POST':
        username: str = request.POST.get('username').strip()
        password: str = request.POST.get('password').strip()

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

#------------------------------------

#TODO: verify SQL injections
def signup(request):
    if request.method == 'POST': #getting forms information
        first_name: str = request.POST.get('first_name').strip()
        last_name: str = request.POST.get('last_name').strip()
        username: str = request.POST.get('username').strip()
        email: str = request.POST.get('email').strip()
        password: str = request.POST.get('password').strip()
        confirm_password: str = request.POST.get('confirm_password').strip()

        print(f"{first_name} {last_name} - {username}: {email} - {password}") # log request signup on terminal

        if password == confirm_password: # verify if password is equal confirm_password and continue
            # username verify
            if not re.fullmatch(USERNAME_PATTERN, username):
                return render(request, 'signup.html', {'error': f'Invalid username'})

            if User.objects.filter(username=username).exists(): # verify if this username is already in use
                return render(request, 'signup.html', {'error': 'Username already in use'})

            # email verify
            if not re.fullmatch(EMAIL_PATTERN, email):
                return render(request, 'signup.html', {'error': f'Invalid email'})

            if User.objects.filter(email=email).exists(): # verify if this email is already in use
                return render(request, 'signup.html', {'error': 'E-mail already in use'})

            # password
            if not re.fullmatch(PASSWORD_PATTERN, password):
                return render(request, 'signup.html', {'error': f'Invalid password'})

            # signup
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

#------------------------------------

def home(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'username': request.user.username})
    else:
        return render(request, 'index-nl.html')
