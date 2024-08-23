from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('properties/', views.properties, name='properties'),
    path('add_property/', views.add_property, name='add_property'),
    path('add_device/', views.add_device, name='add_device'),
]
