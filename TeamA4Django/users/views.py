from base64 import urlsafe_b64encode
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import OptionalInfoForm, CustomUserCreationForm, EditProfileForm
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


###

def create_account_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        optional_info_form = OptionalInfoForm(request.POST)
        if form.is_valid() and optional_info_form.is_valid():
            user = form.save(commit=False) 
            user.is_active = False  # User should not be active until they confirm their email
            # first_name = form.save(first_name)
            user.save()
            profile = optional_info_form.save(commit=False)
            profile.user = user
            profile.save() ##doesn't handle when the username is duplicate! (change to when email is duplicate)

            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
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
            return HttpResponse('Please confirm your email address to complete the registration') #replace with html HERE

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