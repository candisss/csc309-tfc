import re

from django.db import models
from django.db.models import CASCADE
from django.forms import forms


# Create your models here.
class Studio(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    postal_code = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def clean(self):
        phone_regex = re.compile(
            '^\(?([0-9]{3})\)?[-]?([0-9]{3})[-]?([0-9]{4})$')
        postal_regex = re.compile('[A-Z]{1}[0-9]{1}[A-Z]{1}\s*[0-9]{1}[A-Z]{1}['
                                  '0-9]{1}')
        if self.latitude < -90 or self.latitude > 90 or self.longitude < -180 \
                or self.longitude > 180:
            raise forms.ValidationError('Enter a geolocation.')
        if not phone_regex.match(self.phone_num):
            raise forms.ValidationError('Enter a valid phone number.')
        if not postal_regex.match(self.postal_code):
            raise forms.ValidationError('Enter a valid postal code.')



class Amenities(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    type = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return self.type


class Images(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    image = models.ImageField(null=True)
