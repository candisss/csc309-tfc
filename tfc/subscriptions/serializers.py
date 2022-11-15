from rest_framework import serializers
from subscriptions.models import Subscriptions, PaymentCards, PaymentHistory


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ['price', 'term']


class PaymentCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCards
        fields = ['card_holder_name', 'card_num', 'expiry_date', 'postal_code',
                  'billing_address']


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['amount_paid', 'payment_card', 'date', 'time']
