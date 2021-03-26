from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from apps.member.models import Member


class UserAuthenticationMethod(forms.Form):
    AUTH_METHODS = (('email', 'email'), ('sms', 'sms'))
    auth_method = forms.CharField(label='Please choose your authentication method',
                                  widget=forms.RadioSelect(choices=AUTH_METHODS), required=True)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'gender', 'website',
                  'bio']


class UserRegisterSmsForm(UserRegisterForm):
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['phone_number']:
            raise ValidationError('Enter your phone number to receive sms.')


class UserLogInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', max_length=128)


class UserSearch(forms.Form):
    email = forms.CharField(label='Email')


class UserSmsAuthentication(forms.Form):
    token = forms.CharField(label='Code', required=True, max_length=4)
