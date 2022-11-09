import re

from django import forms
from django.core.validators import EmailValidator

from tfc.accounts.models import CustomUser


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    phone_num = forms.CharField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 4:
            self.add_error('username', 'This username is too short. '
                                       'It must contain at least 4'
                                       'characters')

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'A user with that username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != '':
            validator = EmailValidator(message='Enter a valid email address')
            validator(email)
        return email

    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']
        num_regex = re.compile('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
        if not num_regex.match(phone_num):
            self.add_error('phone_num', 'Enter a valid phone number.')
        return phone_num

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != '':
            if len(password1) < 8:
                self.add_error('password1', 'This password is too short. '
                                            'It must contain at least 8 '
                                            'characters')
            if password2 == '':
                self.add_error('password2', "This field is required")
            elif password1 != password2:
                self.add_error('password2', "The two password fields didn't "
                                            "match")

        return cleaned_data
