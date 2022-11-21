import decimal

from rest_framework import serializers

from studios.models import Studio


class StudioInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['name', 'address', 'latitude', 'longitude', 'postal_code',
                  'phone_num']


class DistanceSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)

    def validate_latitude(self, data):
        lat = decimal.Decimal(data)
        if lat < -90 or lat > 90:
            raise serializers.ValidationError('Enter a valid latitude.')
        return lat

    def validate_longitude(self, data):
        lon = decimal.Decimal(data)
        if lon < -180 or lon > 180:
            raise serializers.ValidationError('Enter a valid longitude.')
        return lon
