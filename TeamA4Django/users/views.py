from base64 import urlsafe_b64encode
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import CreditCardForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             # Optionally, add a success message
#             return redirect('profile')  # Redirect to profile page after editing
#     else:
#         form = EditProfileForm(instance=request.user)
#     return render(request, 'edit_profile.html', {'form': form})


from django.core.mail import send_mail
from django.contrib import messages


def home_view(request):
       return render(request, 'index.html')

def logout_view(request):
    logout(request) 
    return redirect('index')

# Original Code
# def create_account_view(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         optional_info_form = OptionalInfoForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False) 
#             user.is_active = False  # User should not be active until they confirm their email
#             # first_name = form.save(first_name)
#             user.save()  
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your SINABOOK ACCOUNT.'

#             message = render_to_string('acc_active_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_b64encode(force_bytes(user.pk)).decode(),
#             'token': account_activation_token.make_token(user),
#                 })
            
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                     mail_subject, message, to=[to_email]
#                 )
#             email.send()
#             if optional_info_form.is_valid():
#                 profile = optional_info_form.save(commit=False)
#                 profile.user = user
#                 profile.subscribe_to_promotions = optional_info_form.cleaned_data.get('subscribe_to_promotions', False)
#                 profile.save()
#                 #create cc object

#             return render(request, 'emailverification.html')

#         else:
#             print(form.errors, optional_info_form.errors)
#     else:
#         form = CustomUserCreationForm()
#         optional_info_form = OptionalInfoForm()

#     return render(request, "createAccount.html", {
#         "form": form,
#         "optional_info_form": optional_info_form
#     })

def index_view(request):
   return render(request, 'index.html')

#The instance of the user is displayed on profile.html with email being an uneditable field
#I cannot check when user is logged out
def profile_view(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = EditProfileForm(request.POST or None, instance = current_user)
        optional_info_form = OptionalInfoForm(request.POST or None, instance = current_user)
        if form.is_valid():
             form.save()
            #  messages.success(request, ("Your profile has been updated!"))
    #    optional_info_form = OptionalInfoForm(request.user)
        if optional_info_form.is_valid():
            optional_info_form.save()

        return render(request, 'profile.html', {'form': form,
                                                "optional_info_form": optional_info_form}) 
    else:
    #    messages.success(request.POST, ("You must be logged in to view this page"))
    #    return redirect ('login')
        return HttpResponse('You must be logged in to view this page')
   


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
            else:
                pass  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registration_confirmation(request):
    return render(request, 'registrationconfirmation.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('registrationconfirmation')
    else:
        return HttpResponse('Activation link is invalid!')
    


def meg_create_account(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)

        print("is user profile form valid: ", user_profile_form.is_valid())
        if not user_profile_form.is_valid():
            print(user_profile_form.errors)

        if user_profile_form.is_valid():
            user = user_profile_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your SINABOOK ACCOUNT.'
            
            message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_b64encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
                })
            
            to_email = user_profile_form.cleaned_data.get('email')
            email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
            email.send()

            if credit_card_form.is_valid() and credit_card_form.cleaned_data:
                credit_card = credit_card_form.save(commit=False)
                credit_card.user = user
                credit_card.save()
                # profile = optional_info_form.save(commit=False)
                # profile.user = user
                # profile.subscribe_to_promotions = optional_info_form.cleaned_data.get('subscribe_to_promotions', False)
                # profile.save()

            return render(request, 'emailverification.html')  # Redirect to account created page or any other page
            

        else:
            print(user_profile_form.errors, credit_card_form.errors)

    else:
        user_profile_form = UserProfileForm()
        credit_card_form = CreditCardForm()

    return render(request, 'createAccount.html', {'user_profile_form': user_profile_form, 'credit_card_form': credit_card_form})

    