from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class OptionalInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'apartment_suite', 'city', 
                  'state_province', 'country', 'zip_postal_code', 'name_on_card', 
                  'card_number', 'expiration', 'cvv', 'billing_zip_postal_code']

