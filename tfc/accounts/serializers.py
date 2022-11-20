import re

from django.contrib.auth import authenticate
from django.db import models

from django.core.validators import EmailValidator
from rest_framework import serializers

from accounts.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'first_name', 'last_name', 'username', 'email',
#                   'phone_num', 'subscribed']


class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(required=True)
    # password2 = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar',
                  'phone_num', 'password', 'password2']

    def validate_username(self, data):
        username = data
        if len(username) < 4:
            raise serializers.ValidationError('This username is too short. '
                                              'It must contain at least 4'
                                              'characters')

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'A user with that username already exists')
        return username

    def validate_email(self, data):
        email = data
        if email != '':
            validator = EmailValidator(message='Enter a valid email address')
            validator(email)
        return email

    def validate_phone_num(self, data):
        phone_num = data
        num_regex = re.compile(
            '^\(?([0-9]{3})\)?[-]?([0-9]{3})[-]?([0-9]{4})$')
        if not num_regex.match(phone_num):
            raise serializers.ValidationError('Enter a valid phone number.')
        return phone_num

    def validate(self, data):
        password = data['password']
        password2 = data['password2']

        if password != '':
            if len(password) < 8:
                raise serializers.ValidationError('This password is too short. '
                                                  'It must contain at least 8 '
                                                  'characters')
            elif password != password2:
                raise serializers.ValidationError(
                    "The two password fields didn't "
                    "match")

        return data

    def create(self, data):
        if 'avatar' in data:
            avatar = data['avatar']
        else:
            avatar = None
        user = CustomUser.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_num=data['phone_num'],
            avatar=avatar,
            username=data['username'],
            email=data['email']
        )

        user.set_password(data['password'])
        user.save()
        return user


# class LoginSerializer(serializers.Serializer):
#     # class Meta:
#     #     model = CustomUser
#     #     fields = ['username', 'password']
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')
#
#         if not username:
#             raise serializers.ValidationError("Username is required")
#         if not password:
#             raise serializers.ValidationError("Password is required")
#
#         user = CustomUser.objects.filter(username=username)
#         if user.exists() and user.count() == 1:
#             user_obj = user.first()
#         else:
#             raise serializers.ValidationError(
#                 "This username/email is not valid.")
#
#         if user_obj:
#             if not user_obj.check_password(password):
#                 raise serializers.ValidationError("Invalid credentials.")
#
#         data['user'] = user_obj
#         return data

class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email']

    def validate_email(self, data):
        email = data
        if email != '':
            validator = EmailValidator(message='Enter a valid email address')
            validator(email)
        return email

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.save()
        return instance


