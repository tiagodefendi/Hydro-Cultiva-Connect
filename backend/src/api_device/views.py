from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from myapp.models import Device, DeviceLog
import json
from datetime import datetime
import numpy as np

# Lives ----------------------------------------------------------------------------

YOUTUBE_LIVE_LINKS = [
    'O0tTOcBrMTI',
    'Na0w3Mz46GA',
    'QKTNfEEeDnE',
    '4oStw0r33so',
    'tNkZsRW7h2c',
    '4xDzrJKXOOY',
    'QviXe8xvA50',
    'ROW9DiPsL98',
    'b_TW4NYsbOo',
    'yOuYY4AL_1U',
]

# Sprinkler ------------------------------------------------------------------------

@csrf_exempt
@require_POST
@login_required(login_url='login')
def turn_on_device(request):
    data = json.loads(request.body)
    device_id = data.get('id')

    try:
        device = Device.objects.get(id=device_id)
        if device.type == 'Sprinkler':
            if device.status != 'On':
                #change
                device.status = 'On'
                device.save()

                #log
                DeviceLog.objects.create(
                    device=device,
                    status='On',
                    interaction_date=datetime.now()
                )
            return JsonResponse({'status': device.status})
        else:
            return JsonResponse({'error': 'Device is not a Sprinkler'}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)

#----------------------

@csrf_exempt
@require_POST
@login_required(login_url='login')
def turn_off_device(request):
    data = json.loads(request.body)
    device_id = data.get('id')

    try:
        device = Device.objects.get(id=device_id)
        if device.type == 'Sprinkler':
            if device.status != 'Off':
                device.status = 'Off'
                device.save()

                DeviceLog.objects.create(
                    device=device,
                    status='Off',
                    interaction_date=datetime.now()
                )
            return JsonResponse({'status': device.status})
        else:
            return JsonResponse({'error': 'Device is not a Sprinkler'}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)

# Tank -------------------------------------------------------------------------------

@csrf_exempt
@require_POST
@login_required(login_url='login')
def check_water(request):
    data = json.loads(request.body)
    device_id = data.get('id')

    try:
        device = Device.objects.get(id=device_id)
        if device.type == 'Tank':
            if device.status != 'Off':
                random = f"{np.clip(np.random.normal(loc=float(device.status[:-1]), scale=10), 0, 100):.2f}%"
            else:
                random = '95%'

            #change
            device.status = random
            device.save()

            #log
            DeviceLog.objects.create(
                device=device,
                status=random,
                interaction_date=datetime.now()
            )
            return JsonResponse({'status': device.status})
        else:
            return JsonResponse({'error': 'Device is not a Tank'}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)

# Thermometer -------------------------------------------------------------------------------

@csrf_exempt
@require_POST
@login_required(login_url='login')
def measure_temperature(request):
    data = json.loads(request.body)
    device_id = data.get('id')

    try:
        device = Device.objects.get(id=device_id)
        if device.type == 'Thermometer':
            if device.status != 'Off':
                random = f"{np.clip(np.random.normal(loc=float(device.status[:-2]), scale=2), 0, 40):.2f}°C"
            else:
                random = '26°C'

            #change
            device.status = random
            device.save()

            #log
            DeviceLog.objects.create(
                device=device,
                status=random,
                interaction_date=datetime.now()
            )
            return JsonResponse({'status': device.status})
        else:
            return JsonResponse({'error': 'Device is not a Thermometer'}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)

# Hygrometer -------------------------------------------------------------------------------

@csrf_exempt
@require_POST
@login_required(login_url='login')
def measure_humidity(request):
    data = json.loads(request.body)
    device_id = data.get('id')

    try:
        device = Device.objects.get(id=device_id)
        if device.type == 'Hygrometer':
            if device.status != 'Off':
                random = f"{np.clip(np.random.normal(loc=float(device.status[:-1]), scale=3), 0, 100):.2f}%"
            else:
                random = '85%'

            #change
            device.status = random
            device.save()

            #log
            DeviceLog.objects.create(
                device=device,
                status=random,
                interaction_date=datetime.now()
            )
            return JsonResponse({'status': device.status})
        else:
            return JsonResponse({'error': 'Device is not a Hygrometer'}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)

@csrf_exempt
@require_POST
@login_required(login_url='login')
def live(request):
    data = json.loads(request.body)
    device_id = data.get('id')

    try:
        device = Device.objects.get(id=device_id)
        if device.type == 'Camera':
            live: str = YOUTUBE_LIVE_LINKS[device.id%10]

            #change
            device.status = 'Live'
            device.save()

            #log
            DeviceLog.objects.create(
                device=device,
                status='Live',
                interaction_date=datetime.now()
            )
            return JsonResponse({'live': live})
        else:
            return JsonResponse({'error': 'Device is not a Camera'}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)
