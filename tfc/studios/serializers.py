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
        lat = data
        if lat < -90 or lat > 90:
            raise serializers.ValidationError('Enter a valid latitude.')

    def validate_longitude(self, data):
        lon = data
        if lon < -90 or lon > 90:
            raise serializers.ValidationError('Enter a valid longitude.')
