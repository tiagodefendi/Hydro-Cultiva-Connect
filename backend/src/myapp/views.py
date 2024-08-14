from django.shortcuts import render, redirect

# TODO: register new user
def signup(request):
    return render(request, 'signup.html')

# TODO: make login logical
def login(request):
    return render(request, 'login.html')

def home(request):
    

    return render(request, 'index.html')
