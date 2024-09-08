from rest_framework import serializers
from myapp.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'property', 'type', 'name', 'key', 'status']
