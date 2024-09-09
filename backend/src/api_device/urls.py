from django.urls import path
from api_device import views

urlpatterns = [
    # General
    path('status_in_period/', views.status_in_period, name='status_in_period'),
    # Sprinkler
    path('turn_on/', views.turn_on_device, name='turn_on_device'),
    path('turn_off/', views.turn_off_device, name='turn_off_device'),
    # Tank
    path('check_water/', views.check_water, name='check_water'),
    # Thermometer
    path('measure_temperature/', views.measure_temperature, name='measure_temperature'),
    # Hygrometer
    path('measure_humidity/', views.measure_humidity, name='measure_humidity'),
    # Camera
    path('live/', views.live, name='live'),
]
