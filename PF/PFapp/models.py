from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Alojamientos(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField()
    address = models.CharField(max_length=256)
    zipcode = models.IntegerField()
    country = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Images(models.Model):
    url = models.URLField()
    alojamiento = models.ForeignKey(Alojamientos)

class Comments(models.Model):
    text = models.TextField()
    date = models.DateTimeField()
    alojamiento = models.ForeignKey(Alojamientos)

class UserSels(models.Model):
    user = models.CharField(max_length=32)
    date = models.DateTimeField()
    alojamiento = models.ForeignKey(Alojamientos)
