from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, CreditCard


class CustomPasswordResetForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password']

class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={'autofocus': True}))
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']  # 'username' is not listed here

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  
        if commit:
            user.save()
        return user

        
class OptionalInfoForm(forms.ModelForm):
    subscribe_to_promotions = forms.BooleanField(required=False)
    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'apartment_suite', 'city', 
                  'state_province', 'country', 'zip_postal_code', 'name_on_card', 
                  'card_number', 'expiration', 'cvv', 'billing_zip_postal_code']
        
        
##Editable information on the profile.html page
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']  # Exclude the user field

        # fields = ['first_name', 'last_name', 'email', 'address_line_1', 'address_line_2', 'apartment_suite', 'city', 
        #           'state_province', 'country', 'zip_postal_code', 'name_on_card', 
        #           'card_number', 'expiration', 'cvv', 'billing_zip_postal_code', 'register_for_promotions']
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Disable editing of email field
        self.fields['email'].disabled = True


class MovieSearchForm(forms.Form):
    title = forms.CharField(label='Search by Title', max_length=100)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        # exclude = ['user']  # Exclude the user field, as it's a OneToOneField
        fields = '__all__'

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = '__all__'  # Include all fields from the CreditCard model



# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)


#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
        

#Original code, 
# class OptionalInfoForm(forms.ModelForm):
#     subscribe_to_promotions = forms.BooleanField(required=False)
#     class Meta:
#         model = UserProfile
#         fields = ['address_line_1', 'address_line_2', 'apartment_suite', 'city', 
#                   'state_province', 'country', 'zip_postal_code', 'name_on_card', 
#                   'card_number', 'expiration', 'cvv', 'billing_zip_postal_code']
        
#Original Code
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)

#     class Meta:
#         model = User
#         fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
        
##Editable information on the profile.html page
#Original Code        
# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         exclude = ['user']  # Exclude the user field

#         fields = ['first_name', 'last_name', 'email', 'address_line_1', 'address_line_2', 'apartment_suite', 'city', 
#                   'state_province', 'country', 'zip_postal_code', 'name_on_card', 
#                   'card_number', 'expiration', 'cvv', 'billing_zip_postal_code', 'subscribe_to_promotions']
#     def __init__(self, *args, **kwargs):
#         super(EditProfileForm, self).__init__(*args, **kwargs)
#         # Disable editing of email field
#         self.fields['email'].disabled = True






