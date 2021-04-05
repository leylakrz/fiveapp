from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from apps.member.models import Member


class UserRegisterForm(UserCreationForm):
    AUTH_METHODS = (('email', 'email'), ('sms', 'sms'))  # member can choose whether they want to be authenticated by
    # receiving an:
    # email containing activation link or
    # sms containing member's generated sms_code.
    auth_method = forms.CharField(label='Please choose your authentication method',
                                  widget=forms.RadioSelect(choices=AUTH_METHODS), required=True)

    class Meta:
        model = Member
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'gender', 'website',
                  'bio', 'auth_method']

    def clean(self):
        cleaned_data = super().clean()
        # if member has chosen authentication by sms, they must have filled the phone_number field.
        if cleaned_data['auth_method'] == 'sms' and not cleaned_data['phone_number']:
            raise ValidationError('Enter your phone number to receive sms.')


class UserLogInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', max_length=128)


class UserSmsAuthentication(forms.Form):
    sms_code = forms.CharField(label='Code', required=False, max_length=4)  # a filed to get the 4 digit sms_code from
    # unauthenticated member after it was sent by sms.
