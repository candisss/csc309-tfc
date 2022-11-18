from django.db import models
from django.db.models import CASCADE


# Create your models here.
class Studio(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    geo_loc = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Amenities(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    type = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return self.type

class Images(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    image = models.ImageField(null=True)
