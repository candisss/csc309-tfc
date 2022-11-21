import decimal
from datetime import date, datetime as dt

import haversine as hs
from django.db.models import Q
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from classes.models import ClassOccurrence
from classes.serializers import ClassOccurrenceSerializer
from studios.models import Amenities, Images, Studio
from studios.serializers import DistanceSerializer, StudioInfoSerializer


# Create your views here.
class StudioInfoView(generics.GenericAPIView):
    serializer_class = StudioInfoSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get(self, request, studio_id):
        # search = request.GET.get('search')
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
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = DistanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        lat = decimal.Decimal(serializer.data.get('latitude'))
        lon = decimal.Decimal(serializer.data.get('longitude'))
        user_loc = (lat, lon)
        distance = []
        for studio in Studio.objects.all():
            studio_loc = (studio.latitude, studio.longitude)
            temp = hs.haversine(user_loc, studio_loc)
            distance.append(temp)
        sorted_studios = [x for _, x in sorted(zip(distance, Studio.objects.all()))]
        studio_list = []
        for i in range(len(sorted_studios)):
            temp = {'name': sorted_studios[i].name,
                    'distance': distance[i]}
            studio_list.append(temp)
        data = {'studio': studio_list}
        return Response(data)


class StudioSearchFilterView(generics.ListAPIView):
    serializer_class = StudioInfoSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Studio.objects.all()
        name = self.request.query_params.get('name')
        amenities = self.request.query_params.get('amenities')
        class_name = self.request.query_params.get('class_name')
        coach = self.request.query_params.get('coach')

        if name:
            queryset = queryset.filter(name=name)
        if amenities:
            queryset = queryset.filter(amenities__type=amenities)
        if class_name:
            queryset = queryset.filter(class_studio__name=class_name)
        if coach:
            queryset = queryset.filter(class_studio__coach=coach)

        return queryset


