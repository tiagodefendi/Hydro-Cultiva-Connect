from django.test import Client
from django.urls import reverse
import json
from myapp.models import Device

def run_check_water_for_all_devices():
    client = Client()
    devices = Device.objects.filter(type='Tank')

    for device in devices:
        response = client.post(reverse('check_water'), json.dumps({'id': device.id}), content_type='application/json')
        # Opcional: Lidar com a resposta, se necessário

def run_measure_temperature_for_all_devices():
    client = Client()
    devices = Device.objects.filter(type='Thermometer')

    for device in devices:
        response = client.post(reverse('measure_temperature'), json.dumps({'id': device.id}), content_type='application/json')
        # Opcional: Lidar com a resposta, se necessário

def run_measure_humidity_for_all_devices():
    client = Client()
    devices = Device.objects.filter(type='Hygrometer')

    for device in devices:
        response = client.post(reverse('measure_humidity'), json.dumps({'id': device.id}), content_type='application/json')
        # Opcional: Lidar com a resposta, se necessário

def run_all_device_tasks():
    run_check_water_for_all_devices()
    run_measure_temperature_for_all_devices()
    run_measure_humidity_for_all_devices()
