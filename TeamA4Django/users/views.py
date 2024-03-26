from base64 import urlsafe_b64encode
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import CustomUserCreationForm, OptionalInfoForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages


def home_view(request):
       return render(request, 'index.html')

def logout_view(request):
    logout(request) 
    return redirect('index')

def create_account_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        optional_info_form = OptionalInfoForm(request.POST)
        if form.is_valid() and optional_info_form.is_valid():
            user = form.save(commit=False) 
            user.is_active = False  # User should not be active until they confirm their email
            user.save()
            profile = optional_info_form.save(commit=False)
            profile.user = user
            profile.subscribe_to_promotions = optional_info_form.cleaned_data.get('subscribe_to_promotions', False)
            profile.save()
  
            current_site = get_current_site(request)
            mail_subject = 'Activate your SINABOOK ACCOUNT.'

            message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_b64encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
                })
            
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
            email.send()
            return render(request, 'emailverification.html')

        else:
            print(form.errors, optional_info_form.errors)
    else:
        form = CustomUserCreationForm()
        optional_info_form = OptionalInfoForm()

    return render(request, "createAccount.html", {
        "form": form,
        "optional_info_form": optional_info_form
    })

def index_view(request):
   return render(request, 'index.html')

def profile_view(request):
   return render(request, 'profile.html')

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
    