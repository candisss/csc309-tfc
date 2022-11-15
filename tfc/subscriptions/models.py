from django.db import models
from django.db.models import CASCADE


# Create your models here.
class Subscriptions(models.Model):
    price = models.CharField(max_length=50)
    # term can only be "year" or "month"
    term = models.CharField(max_length=50)

class PaymentCards(models.Model):
    card_holder_name = models.CharField(max_length=100)
    card_num = models.CharField(max_length=50)
    expiry_date = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=100)

class PaymentHistory(models.Model):
    amount_paid = models.CharField(max_length=50)
    payment_card = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()


