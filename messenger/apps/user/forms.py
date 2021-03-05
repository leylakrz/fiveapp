from django import forms
from django.core.exceptions import ValidationError

from apps.user.models import User


class UserRegisterForm(forms.ModelForm):
    password_repeat = forms.CharField(label='Repeat Password', max_length=50)

    class Meta:
        model = User
        exclude = ['salt', 'register_time', 'following']

    def clean(self):
        cleaned_data = super().clean()
        password, password_repeat = cleaned_data['password'], cleaned_data['password_repeat']
        if password != password_repeat:
            raise ValidationError("password fields are not the same.")


class UserLogInForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', max_length=50)


class UserSearch(forms.Form):
    email = forms.CharField(label='Email')
