import re

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
import re

from subscriptions.models import Subscription, PaymentCard, PaymentHistory


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['price', 'term']


class PaymentHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentHistory
        fields = ['amount_paid', 'payment_card', 'datetime', 'user']

    def validate_card_num(self, data):
        card_num = data
        num_regex = re.compile('\d{16}')
        if not num_regex.match(card_num):
            raise serializers.ValidationError('Enter a valid card number.')
        return card_num

    def validate_expiry_date(self, data):
        expiry_date = data
        date_regex = re.compile('^(0[1-9]|1[0-2])\/?([0-9]{2})$')
        if not date_regex.match(expiry_date):
            raise serializers.ValidationError('Enter a valid expiry date.')
        return expiry_date

    def validate_postal_code(self, data):
        postal_code = data
        postal_regex = re.compile('[A-Z]{1}[0-9]{1}[A-Z]{1}\s*[0-9]{1}[A-Z]{1}['
                                  '0-9]{1}')
        if not postal_regex.match(postal_code):
            raise serializers.ValidationError('Enter a valid postal code.')
        return postal_code

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(PaymentCardSerializer, self).create(validated_data)


class PaymentCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentCard
        fields = ['card_holder_name', 'card_num', 'expiry_date', 'postal_code',
                  'billing_address', 'user']
        read_only_fields = ['user']

    def validate_card_num(self, data):
        card_num = data
        num_regex = re.compile('\d{16}')
        if not num_regex.match(card_num):
            raise serializers.ValidationError('Enter a valid card number.')
        return card_num

    def validate_expiry_date(self, data):
        expiry_date = data
        date_regex = re.compile('^(0[1-9]|1[0-2])\/?([0-9]{2})$')
        if not date_regex.match(expiry_date):
            raise serializers.ValidationError('Enter a valid expiry date.')
        return expiry_date
