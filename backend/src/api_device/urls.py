from django.urls import path
from api_device import views

urlpatterns = [
    path('turn_on/', views.turn_on_device, name='turn_on_device'),
    path('turn_off/', views.turn_off_device, name='turn_off_device'),
    path('check_water/', views.check_water, name='check_water'),
    path('measure_temperature/', views.measure_temperature, name='measure_temperature'),
    path('measure_humidity/', views.measure_humidity, name='measure_humidity'),
    path('live/', views.live, name='live'),
]