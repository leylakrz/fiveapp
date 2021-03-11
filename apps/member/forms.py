from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.member.models import Member


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['email', 'first_name', 'last_name', 'gender', 'website',
                  'bio']


class UserLogInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', max_length=128)


class UserSearch(forms.Form):
    email = forms.CharField(label='Email')
