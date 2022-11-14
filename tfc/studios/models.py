from django.db import models

# Create your models here.
class Studio(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    geo_loc = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=100)
