import re

from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email',
                  'phone_num', 'subscribed']


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email',
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
            '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
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
            email=data['email'],
            subscribed=False
        )

        user.set_password(data['password'])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def validate(self, data):
        username = data['username']
        password = data['password']

        if not username:
            raise serializers.ValidationError("Username is required")
        if not password:
            raise serializers.ValidationError("Password is required")
        if not (user := authenticate(username=username, password=password)):
            raise serializers.ValidationError(
                    'Username or password is invalid')
        data['user'] = user
        return data
