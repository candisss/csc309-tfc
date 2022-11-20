from rest_framework import serializers

from studios.models import Studio


class StudioInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['name', 'address', 'latitude', 'longitude', 'postal_code',
                  'phone_num']


class DistanceSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

# class StudioSearchSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     amenities = serializers.CharField(max_length=100)
#     class_name = serializers.CharField(max_length=100)
#     coach = serializers.CharField(max_length=100)
