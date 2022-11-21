from django.db import models
from django.db.models import CASCADE, SET_NULL

from accounts.models import CustomUser

SUBSCRIPTION_LENGTH_CHOICES = (
    ("YEAR", "Year"),
    ("MONTH", "Month"),
)


# Create your models here.
class Subscription(models.Model):
    price = models.CharField(max_length=50)
    # term can only be "year" or "month"
    term = models.CharField(max_length=10, choices=SUBSCRIPTION_LENGTH_CHOICES)

    def __str__(self):
        return str(self.price) + str(self.term)


class PaymentCard(models.Model):
    card_holder_name = models.CharField(max_length=100)
    card_num = models.CharField(max_length=50)
    expiry_date = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=100)
    user = models.OneToOneField(to=CustomUser, on_delete=CASCADE,
                                related_name='payment_card')

    def __str__(self):
        return str(self.card_holder_name) + str(self.card_num)


class PaymentHistory(models.Model):
    amount_paid = models.CharField(max_length=50)
    payment_card = models.ForeignKey(to=PaymentCard, on_delete=SET_NULL, null=True, blank=True, related_name='payment_card')
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=CustomUser, on_delete=CASCADE,
                             related_name='payment_histories')

    def __str__(self):
        return str(self.amount_paid) + self.datetime.__str__()
