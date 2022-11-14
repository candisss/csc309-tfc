import jwt
from django.contrib.auth import login
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, RetrieveAPIView, \
    UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
from accounts.serializers import LoginSerializer, RegisterSerializer


# Create your views here.
# class RegisterView(GenericAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user": CustomUserSerializer(user,
#                                          context=self.get_serializer_context()).data
#         })
#
#
# class LoginView(GenericAPIView):
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         serializer = self.get_serializer(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return Response({"user": CustomUserSerializer(user,
#                                                       context=self.get_serializer_context()).data
#                          })
#
#
# # class UserView(RetrieveAPIView, UpdateAPIView):
#     serializer_class = CustomUserSerializer
#
#     def get_object(self):
#         serializer = CustomUserSerializer(self.request.user)
#         return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"status": status.HTTP_200_OK, "Token": token.key})
