import jwt
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.generics import GenericAPIView, RetrieveAPIView, \
    UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts import serializers
from accounts.models import CustomUser
from accounts.serializers import LoginSerializer, RegisterSerializer, \
    CustomUserSerializer


# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": CustomUserSerializer(user,
                                         context=self.get_serializer_context()).data
        })


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"user": CustomUserSerializer(user,
                                                      context=self.get_serializer_context()).data
                         })


class UserView(RetrieveAPIView, UpdateAPIView):
    serializer_class = CustomUserSerializer

    def get_object(self):
        serializer = CustomUserSerializer(self.request.user)
        return Response(serializer.data)
