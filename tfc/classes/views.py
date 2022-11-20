import json
from datetime import datetime as dt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
from classes.models import Class
from classes.serializers import ClassOccurrenceSerializer


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


class ClassHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        class_history = user.class_occurrence_students_enrolled.exclude(cancelled=True).filter(date__lt=dt.now()).order_by('date')
        history_serializer = ClassOccurrenceSerializer(class_history, many=True)

        return Response({'History': history_serializer.data})


class ClassScheduleView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        class_history = user.class_occurrence_students_enrolled.exclude(cancelled=True).filter(date__gte=dt.now()).order_by('date')
        history_serializer = ClassOccurrenceSerializer(class_history, many=True)

        return Response({'Schedule': history_serializer.data})
