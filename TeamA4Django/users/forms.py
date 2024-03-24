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
    subscribe_to_promotions = forms.BooleanField(required=False)
    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'apartment_suite', 'city', 
                  'state_province', 'country', 'zip_postal_code', 'name_on_card', 
                  'card_number', 'expiration', 'cvv', 'billing_zip_postal_code']
        

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'address_line_1', 'address_line_2']

