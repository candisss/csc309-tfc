from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()
        if not (user := authenticate(username=data.get('username'),
                                     password=data.get('password'))):
            self.add_error('password', 'Username or password is invalid')

        data['user'] = user

        return data


