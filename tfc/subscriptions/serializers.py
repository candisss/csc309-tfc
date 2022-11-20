from rest_framework import serializers
from subscriptions.models import Subscription, PaymentCard, PaymentHistory


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['price', 'term']


class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = ['card_holder_name', 'card_num', 'expiry_date', 'postal_code',
                  'billing_address']


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['amount_paid', 'payment_card', 'datetime']
