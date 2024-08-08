from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([name, email, password, confirm_password]):
            return render(request, 'signup.html', {'error': 'Todos os campos são obrigatórios.'})

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'As senhas não coincidem.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Este email já está registrado.'})

        user = User(username=name, email=email, password=make_password(password))
        user.save()

        return redirect('login')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')  # Redirecione para a URL nomeada 'home'
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'index.html')