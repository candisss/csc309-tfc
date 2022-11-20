from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from subscriptions.models import Subscription, PaymentCard, PaymentHistory


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['price', 'term']


class PaymentCardSerializer(serializers.ModelSerializer):
    user = CurrentUserDefault()

    class Meta:
        model = PaymentCard
        fields = ['card_holder_name', 'card_num', 'expiry_date', 'postal_code',
                  'billing_address', 'user']


class PaymentHistorySerializer(serializers.ModelSerializer):
    user = CurrentUserDefault()

    class Meta:
        model = PaymentHistory
        fields = ['amount_paid', 'payment_card', 'datetime', 'user']
