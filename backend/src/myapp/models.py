from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()
    latitude: models.FloatField = models.FloatField() # -24.061395
    longitude: models.FloatField = models.FloatField() # -52.386181

    def __str__(self) -> str:
        return f'{self.name} ({self.latitude}, {self.longitude})'

class Device(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='devices')
    type: models.CharField = models.CharField(max_length=100)
    name: models.CharField = models.CharField(max_length=100)
    key: models.CharField = models.CharField(max_length=17) # T3ST3-T3ST3-T3ST3

    def __str__(self) -> str:
        return f'{self.name: {self.type}}'
