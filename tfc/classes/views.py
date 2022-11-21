import json
from datetime import datetime as dt

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
from classes.models import Class
from classes.serializers import ClassOccurrenceSerializer

from classes.models import ClassOccurrence


class EnrollStudentsView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        class_id = data.get('class_id')
        enrol_type = data.get('type')
        date_str = data.get('date')
        try:
            class_obj = Class.objects.get(id=class_id)
            assert user.subscribed
            if enrol_type == 'single':
                date_obj = dt.strptime(date_str, '%Y-%m-%d').date()
                if date_obj > dt.today().date():
                    class_occurrence_queryset = class_obj.class_occurrence_class_obj.filter(cancelled=False, date=date_obj)
                    if class_occurrence_queryset.exists():
                        class_occurrence = class_occurrence_queryset.first()
                        students_enrolled = class_occurrence.students_enrolled.all()
                        if len(students_enrolled) < class_obj.capacity:
                            if user not in students_enrolled:
                                class_occurrence.students_enrolled.add(user)
                                class_occurrence.save()
                                response_msg = {'detail': f'You have successfully enrolled in {class_obj} on {date_obj.strftime("%b %d %Y")}.'}
                                response_code = status.HTTP_200_OK
                            else:
                                response_msg = {'detail': f'You are already enrolled in {class_obj} on {date_obj.strftime("%b %d %Y")}.'}
                                response_code = status.HTTP_400_BAD_REQUEST
                        else:
                            response_msg = {'detail': 'The class already is full.'}
                            response_code = status.HTTP_400_BAD_REQUEST
                    else:
                        response_msg = {'detail': f'There is no {class_obj} class on {date_obj.strftime("%b %d %Y")}.'}
                        response_code = status.HTTP_400_BAD_REQUEST
                else:
                    response_msg = {'detail': f'You can\'t enroll in past classes!'}
                    response_code = status.HTTP_400_BAD_REQUEST
            elif enrol_type == 'all':
                if not class_obj.is_full():
                    class_occurrence_queryset = class_obj.class_occurrence_class_obj.filter(cancelled=False, date__gt=dt.today().date())
                    if class_occurrence_queryset.exists():
                        for class_occurrence in class_occurrence_queryset:
                            class_occurrence.students_enrolled.add(user)
                            class_occurrence.save()
                        response_msg = {'detail': f'You have successfully enrolled in all the future classes of {class_obj}.'}
                        response_code = status.HTTP_200_OK
                    else:
                        response_msg = {'detail': f'There are no {class_obj} classes in the future!'}
                        response_code = status.HTTP_400_BAD_REQUEST
                else:
                    response_msg = {'detail': 'The class already is full.'}
                    response_code = status.HTTP_400_BAD_REQUEST
            else:
                response_msg = {'detail': f'Invalid enroll type!'}
                response_code = status.HTTP_400_BAD_REQUEST
        except AssertionError:
            response_msg = {'detail': 'You don\' have an active subscription!'}
            response_code = status.HTTP_400_BAD_REQUEST
        except Class.DoesNotExist:
            response_msg = {'detail': 'Invalid class id!'}
            response_code = status.HTTP_400_BAD_REQUEST

        return Response(response_msg, response_code)


class DropStudentsView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        class_id = data.get('class_id')
        drop_type = data.get('type')
        date_str = data.get('date')
        try:
            class_obj = Class.objects.get(id=class_id)
            assert user.subscribed
            if drop_type == 'single':
                date_obj = dt.strptime(date_str, '%Y-%m-%d').date()
                if date_obj > dt.today().date():
                    class_occurrence_queryset = class_obj.class_occurrence_class_obj.filter(cancelled=False, date=date_obj)
                    if class_occurrence_queryset.exists():
                        class_occurrence = class_occurrence_queryset.first()
                        students_enrolled = class_occurrence.students_enrolled.all()
                        if user in students_enrolled:
                            class_occurrence.students_enrolled.remove(user)
                            class_occurrence.save()
                            response_msg = {'detail': f'You have successfully dropped from {class_obj} on {date_obj.strftime("%b %d %Y")}.'}
                            response_code = status.HTTP_200_OK
                        else:
                            response_msg = {'detail': f'You are not in {class_obj} on {date_obj.strftime("%b %d %Y")}.'}
                            response_code = status.HTTP_400_BAD_REQUEST
                    else:
                        response_msg = {'detail': f'There is no {class_obj} class on {date_obj.strftime("%b %d %Y")}.'}
                        response_code = status.HTTP_400_BAD_REQUEST
                else:
                    response_msg = {'detail': f'You can\'t drop from past classes'}
                    response_code = status.HTTP_400_BAD_REQUEST
            elif drop_type == 'all':
                class_occurrence_queryset = class_obj.class_occurrence_class_obj.filter(cancelled=False, date__gt=dt.today().date())
                if class_occurrence_queryset.exists():
                    for class_occurrence in class_occurrence_queryset:
                        class_occurrence.students_enrolled.remove(user)
                        class_occurrence.save()
                    response_msg = {'detail': f'You have successfully dropped from all the future classes of {class_obj}.'}
                    response_code = status.HTTP_200_OK
                else:
                    response_msg = {'detail': f'There are no {class_obj} classes in the future!'}
                    response_code = status.HTTP_400_BAD_REQUEST
            else:
                response_msg = {'detail': f'Invalid drop type!'}
                response_code = status.HTTP_400_BAD_REQUEST
        except AssertionError:
            response_msg = {'detail': 'You don\' have an active subscription!'}
            response_code = status.HTTP_400_BAD_REQUEST
        except Class.DoesNotExist:
            response_msg = {'detail': 'Invalid class id!'}
            response_code = status.HTTP_400_BAD_REQUEST

        return Response(response_msg, response_code)


class ClassHistoryView(generics.GenericAPIView):
    pagination_class = PageNumberPagination
    def get(self, request, *args, **kwargs):
        user = request.user
        class_history = user.class_occurrence_students_enrolled.exclude(cancelled=True).filter(date__lt=dt.now()).order_by('date')
        history_serializer = ClassOccurrenceSerializer(class_history, many=True)

        return self.get_paginated_response(self.paginate_queryset(history_serializer.data))


class ClassScheduleView(generics.GenericAPIView):
    pagination_class = PageNumberPagination
    def get(self, request, *args, **kwargs):
        user = request.user
        class_history = user.class_occurrence_students_enrolled.exclude(cancelled=True).filter(date__gte=dt.now()).order_by('date')
        history_serializer = ClassOccurrenceSerializer(class_history, many=True)

        return self.get_paginated_response(self.paginate_queryset(history_serializer.data))


class ClassSearchFilterView(generics.ListAPIView):
    serializer_class = ClassOccurrenceSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = ClassOccurrence.objects.all()
        studio_name = self.request.query_params.get('studio_name')
        class_name = self.request.query_params.get('class_name')
        coach = self.request.query_params.get('coach')
        date = self.request.query_params.get('date')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        if studio_name:
            queryset = queryset.filter(class_obj__studio__name=studio_name)
        if class_name:
            queryset = queryset.filter(class_obj__name=class_name)
        if coach:
            queryset = queryset.filter(class_obj__coach=coach)
        if date:
            queryset = queryset.filter(date=date)
        if start_time:
            time_search = dt.strptime(start_time, '%H:%M %p').time()
            queryset = queryset.filter(Q(class_obj__start_time__gte=time_search))
        if end_time:
            time_search = dt.strptime(end_time, '%H:%M %p').time()
            queryset = queryset.filter(Q(class_obj__end_time__lte=time_search))

        return queryset
