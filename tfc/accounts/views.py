from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render
from rest_framework import permissions
from rest_framework.generics import GenericAPIView, RetrieveAPIView, \
    UpdateAPIView
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.views import APIView

from tfc.accounts import serializers
from tfc.accounts.models import CustomUser
from tfc.accounts.serializers import RegisterSerializer, UserSerializer


# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.LoginSerializer(data=self.request.data,
                                                 context={
                                                     'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"user": UserSerializer(user, context={
                                                     'request': self.request}).data,
                         "token": AuthToken.objects.create(user)[1]})


class UserView(RetrieveAPIView, UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.kwargs['id'])
