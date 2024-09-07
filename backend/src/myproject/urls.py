from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('', views.home, name='home'),
    # account
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('recover_password/', views.recover_password, name='recover_password'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/change_password/', views.change_password, name='change_password'),
    path('profile/<str:username>/delete_account/', views.delete_account, name='delete_account'),
    # properties
    path('properties/', views.properties, name='properties'), # map
    path('add_property/', views.add_property, name='add_property'),
    path('properties/<int:property_id>/', views.property, name='property'),
    path('properties/<int:property_id>/edit/', views.edit_property, name='edit_property'),
    path('properties/<int:property_id>/delete/', views.delete_property, name='delete_property'),
    #devices
    path('properties/<int:id>/add_device/', views.add_device, name='add_device'),
    path('properties/<int:property_id>/device/<int:device_id>/', views.device, name='device'),
    path('properties/<int:property_id>/device/<int:device_id>/edit/', views.edit_device, name='edit_device'),
    path('properties/<int:property_id>/device/<int:device_id>/delete/', views.delete_device, name='delete_device'),
]
