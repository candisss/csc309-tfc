from django.http import HttpResponse
from django.shortcuts import render
import haversine as hs
import decimal
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from studios.serializers import StudioInfoSerializer

from studios.models import Studio

from studios.models import Amenities

from studios.models import Images

from studios.serializers import DistanceSerializer


# Create your views here.
class StudioInfoView(generics.GenericAPIView):
    serializer_class = StudioInfoSerializer
    permission_classes = (AllowAny,)

    def get(self, request, studio_id):
        if not Studio.objects.filter(id=studio_id).exists():
            return Response('NOT FOUND', status=404)
        else:
            studio = Studio.objects.get(id=studio_id)

            all_amenities = Amenities.objects.filter(studio=studio.id).all()
            amenities_list = []
            for item in all_amenities:
                temp = {'type': item.type,
                        'quantity': item.quantity}
                amenities_list.append(temp)

            all_images = Images.objects.filter(studio=studio.id).all()
            images_list = []
            for item in all_images:
                temp = {'image': item.image.url}
                images_list.append(temp)

            data = {'name': studio.name,
                    'address': studio.address,
                    'latitude': studio.latitude,
                    'longitude': studio.longitude,
                    'postal_code': studio.postal_code,
                    'phone_num': studio.phone_num,
                    'amenities': amenities_list,
                    'images': images_list
                    }
            return Response(data)


class ListbyDistanceView(generics.GenericAPIView):
    serializer_class = DistanceSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        lat = decimal.Decimal(float(request.POST.get('latitude')))
        lon = decimal.Decimal(float(request.POST.get('longitude')))
        user_loc = (lat, lon)
        distance = []
        for studio in Studio.objects.all():
            studio_loc = (studio.latitude, studio.longitude)
            temp = hs.haversine(user_loc, studio_loc)
            distance.append(temp)
        sorted_studios = [x for _,x in sorted(zip(distance, Studio.objects.all()))]
        studio_list = []
        for i in range(len(sorted_studios)):
            temp = {'name': sorted_studios[i].name,
                    'distance': distance[i]}
            studio_list.append(temp)
        data = {'studio': studio_list}
        return Response(data)
