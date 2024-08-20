from django.shortcuts import render, redirect

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

# TODO: register new user
def signup(request):
    return render(request, 'signup.html')

# TODO: make login logical
def login(request):
    return render(request, 'login.html')

def home(request):


    return render(request, 'index.html')
