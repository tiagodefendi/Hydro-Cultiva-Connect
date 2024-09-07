from django.urls import path
from api_device import views

urlpatterns = [
    path('turn_on/', views.turn_on_device, name='turn_on_device'),
    path('turn_off/', views.turn_off_device, name='turn_off_device'),
]