from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, CreditCard, Movie, Show, Showtimes, Promotions
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
import os
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken


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

 # delete later - alexis       
class OptionalInfoForm(forms.ModelForm):
    subscribe_to_promotions = forms.BooleanField(required=False)
    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'apartment_suite', 'city', 
                  'state_province', 'country', 'zip_postal_code', 'name_on_card', 
                  'card_number', 'expiration', 'cvv', 'billing_zip_postal_code']
        
        
##Editable information on the profile.html page
        
class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'address_line_1', 'address_line_2', 'city', 'state_province', 'country', 'zip_postal_code', 'subscribe_to_promotions']



class MovieSearchForm(forms.Form):
    title = forms.CharField(label='Search by Title', max_length=100)

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']

# class UserProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'  
#         exclude = ['user', 'email', 'password'] 
        

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = '__all__'  
        exclude = ['user_profile']

        widgets = {
           'card_number': forms.TextInput(attrs={'required': False}),
         }
    
    def __init__(self, *args, **kwargs):
            super(CreditCardForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].required = False


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'duration', 'trailer_url', 'image', 'genre']
        labels = {
            'title': 'Title',
            'description': 'Description',
           
        }

        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}), 
        }

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration <= 0:
            raise forms.ValidationError("Duration must be a positive number of minutes.")
        return duration

class PromotionsForm(forms.ModelForm):
    class Meta:
        model = Promotions
        fields = ['code', 'percentage', 'start_date', 'end_date', 'show', 'is_available']

# meg- commmented out just incase 
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



class ShowAdminForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        showtime_id = cleaned_data.get('showtime').id
        showroom = cleaned_data.get('showroom')

        # Validate showtime assignment
        new_showtime = Showtimes.objects.get(id=showtime_id)
        conflicting_show = Show.objects.filter(
            showroom=showroom,
            showtime__date=new_showtime.date,
            showtime__time_slot=new_showtime.time_slot
        ).exclude(id=self.instance.id).exists()

        if conflicting_show:
            raise ValidationError({
                'showtime': "This time slot in the selected showroom is already booked."
            })

        return cleaned_data


from django import forms
from .models import UserProfile

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'address_line_1', 'address_line_2', 'apartment_suite', 'city', 
                  'state_province', 'country', 'zip_postal_code', 'name_on_card', 
                  'card_number', 'expiration', 'cvv', 'billing_zip_postal_code', 'subscribe_to_promotions']
    
    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        # Add any custom initialization code here

    def clean_card_number(self):
        card_number = self.initial.get('card_number', '')  # Get initial value of card_number
        if card_number:
            card_number = card_number.strip()[2:-1]
            key = os.environ.get('FERNET_KEY')
            fernet = Fernet(key)
            try:
                decrypted_card_number = fernet.decrypt(card_number.encode()).decode()
            except InvalidToken:
                decrypted_card_number = "Invalid Card Number"
        else:
            decrypted_card_number = ""
        return decrypted_card_number


    def clean_cvv(self):
        cvv = self.initial.get('cvv', '')  # Get initial value of cvv
        if cvv:
            cvv = cvv.strip()[2:-1]
            key = os.environ.get('FERNET_KEY')
            fernet = Fernet(key)
            try:
                decrypted_cvv = fernet.decrypt(cvv.encode()).decode()
            except InvalidToken:
                decrypted_cvv = "Invalid CVV"
        else:
            decrypted_cvv = ""
        return decrypted_cvv