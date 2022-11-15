from django.db import models
from django.db.models import CASCADE

from accounts.models import CustomUser


# Create your models here.
class Subscription(models.Model):
    price = models.CharField(max_length=50)
    # term can only be "year" or "month"
    term = models.CharField(max_length=50)

    def __str__(self):
        return self.price, self.term


class PaymentCard(models.Model):
    card_holder_name = models.CharField(max_length=100)
    card_num = models.CharField(max_length=50)
    expiry_date = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=100)
    user = models.ForeignKey(to=CustomUser, on_delete=CASCADE,
                             related_name='payment_cards')

    def __str__(self):
        return self.card_holder_name, self.card_num


class PaymentHistory(models.Model):
    amount_paid = models.CharField(max_length=50)
    payment_card = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    user = models.ForeignKey(to=CustomUser, on_delete=CASCADE,
                             related_name='payment_cards')

    def __str__(self):
        return self.amount_paid, self.datetime.__str__()
