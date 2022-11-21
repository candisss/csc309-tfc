from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.models import CustomUser
from accounts.serializers import RegisterSerializer, EditProfileSerializer

from accounts.serializers import PasswordResetSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EditProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EditProfileSerializer

    def get_object(self):
        return self.request.user


class PasswordResetView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordResetSerializer

    def get_object(self):
        return self.request.user
