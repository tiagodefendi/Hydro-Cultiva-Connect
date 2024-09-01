from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('', views.home, name='home'),
    # account
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    # properties
    path('properties/', views.properties, name='properties'), # map
    path('properties/<int:id>/', views.property, name='property'),
    path('add_property/', views.add_property, name='add_property'),
    #devices
    path('properties/<int:id>/add_device/', views.add_device, name='add_device'),
]
