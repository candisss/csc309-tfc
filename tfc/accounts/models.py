from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    subscribed = models.BooleanField()
    avatar = models.ImageField(required=False)
