from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from myapp.models import Device, DeviceLog
import json
from datetime import datetime

# Sprinkler ------------------------------------------------------------------------

@csrf_exempt
@require_POST
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