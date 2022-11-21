import re
from django.core.validators import EmailValidator
from rest_framework import serializers

from accounts.models import CustomUser



class RegisterSerializer(serializers.ModelSerializer):

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


class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_num', 'avatar']

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

    # def update(self, instance, validated_data):
    #     instance.email = validated_data['email']
    #     instance.first_name = validated_data['first_name']
    #     instance.last_name = validated_data['last_name']
    #     instance.phone_num = validated_data['phone_num']
    #     instance.avatar = validated_data['avatar']
    #     instance.save()
    #     return instance


class PasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate_old_password(self, data):
        user = self.context['request'].user
        if not user.check_password(data):
            raise serializers.ValidationError({"old_password": "Old password "
                                                               "is "
                                                               "incorrect"})
        return data

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "The two password "
                                                           "fields didn't "
                                                           "match."})
        return data

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


