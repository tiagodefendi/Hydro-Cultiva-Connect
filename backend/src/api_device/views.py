from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from myapp.models import Device
import json

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
                device.status = 'On'
                device.save()
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
            return JsonResponse({'status': device.status})
        else:
            return JsonResponse({'error': 'Device is not a Sprinkler'}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)
