from django.db import models

class Property(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()
    latitude: models.FloatField = models.FloatField()
    longitude: models.FloatField = models.FloatField()

    def __str__(self) -> str:
        return self.name

class Devices(models.Model):
    type: models.CharField = models.CharField(max_length=100)
    name: models.CharField = models.CharField(max_length=100)
    key: models.CharField = models.CharField(max_length=11)
