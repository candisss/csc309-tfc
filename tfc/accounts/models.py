from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    subscribed = models.BooleanField(null=True)
    avatar = models.ImageField(null=True)
    phone_num = models.CharField(max_length=15)
