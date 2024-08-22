from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login


def add_device(request):
    if request.method == 'POST':
        id = 1
        type = request.POST.get('type')
        name = request.POST.get('name')
        key = request.POST.get('key')

        print(f'{type}-{id}: {name} = {key}')
    return render(request, 'add_device.html')

def add_property(request):
    return render(request, 'add_property.html')

def properties(request):
    return render(request, 'properties.html')

#TODO: verify SQL injections
def signup(request):
    if request.method == 'POST':
        first_name: str = request.POST.get('first_name')
        last_name: str = request.POST.get('last_name')
        username: str = request.POST.get('username')
        email: str = request.POST.get('email')
        password: str = request.POST.get('password')
        confirm_password: str = request.POST.get('confirm_password')

        print(f"{first_name} {last_name} - {username}: {email} - {password}")

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                    return render(request, 'signup.html', {'error': 'Username already in use'})

            if User.objects.filter(email=email).exists():
                    return render(request, 'signup.html', {'error': 'E-mail already in useo'})

            try:
                user:User = User.objects.create_user(
                    first_name = first_name,
                    last_name= last_name,
                    username=username,
                    email=email,
                    password=password
                    )

                user.save()

                return redirect('login')
            except Exception as e:
                return render(request, 'signup.html', {'error': f'{e}'})
        else:
            return render(request, 'signup.html', {'error': 'Passwords don\'t match'})


    return render(request, 'signup.html')

# TODO: make login logical
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

def home(request):


    return render(request, 'index.html')
