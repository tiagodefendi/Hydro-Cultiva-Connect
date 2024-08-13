from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login

# TODO: register new user
def signup(request):
    return render(request, 'signup.html')

# TODO: make login logical
def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'index.html')
