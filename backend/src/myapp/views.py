from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login


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
        username: str = request.POST.get('name')
        email: str = request.POST.get('email')
        password: str = request.POST.get('password')
        confirm_password: str = request.POST.get('confirm_password')

        print(username, '-', email, ':', password, confirm_password, '=?', confirm_password==password)

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                    return render(request, 'signup.html', {'error': 'Nome de usuário já existe'})

            if User.objects.filter(email=email).exists():
                    return render(request, 'signup.html', {'error': 'E-mail já está em uso'})

            try:
                user:User = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                return redirect('login')
            except:
                return render(request, 'signup.html', {'error': 'Usuário já existe'})
        else:
            return render(request, 'signup.html', {'error': 'As senhas não coincidem'})


    return render(request, 'signup.html')

# TODO: make login logical
def login(request):
    return render(request, 'login.html')

def home(request):


    return render(request, 'index.html')
