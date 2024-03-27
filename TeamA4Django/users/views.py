from base64 import urlsafe_b64encode
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
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
from .models import Movie
from .forms import MovieSearchForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordResetForm


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




def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('index')  # Redirect to a confirmation page or home
    else:
        form = CustomPasswordResetForm(user=request.user)
    return render(request, 'registration/password_reset_confirm.html', {'form': form})

def home_view(request):
       return render(request, 'index.html')

def logout_view(request):
    logout(request) 
    return redirect('index')


def admin_login_view(request):
    # If the request is POST, try to pull out the relevant info.
    if request.method == 'POST':
        # Create an instance of the form filled with the submitted data
        form = AuthenticationForm(request, data=request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # Get the username and password from the valid form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
    
            user = authenticate(username=username, password=password)
            # If we have a user 
            if user is not None:
                # Check if user is an admin
                if user.is_superuser:
                    # Log the user in
                    login(request, user)
                    # Redirect to the admin home page
                    return redirect('admin-home')  # Make sure 'admin-home' is the correct path name in your urls.py
                else:
                    # If the user exists but is not an admin, show an error message
                    messages.error(request, 'Login failed: You are not an admin.')
            else:
                # No user returned by authenticate, show an error message
                messages.error(request, 'Login failed: Invalid username or password.')
        else:
            # Form is not valid, show an error message
            messages.error(request, 'Login failed: Invalid form input.')
    else:
        # If the request is not POST, create a blank authentication form
        form = AuthenticationForm()

    # Render the page with the login form (whether blank or with errors)
    return render(request, 'admin/adminlogin.html', {'form': form})

   


def admin_home_view(request):
     return render(request, 'adminHome.html')


def create_account_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        optional_info_form = OptionalInfoForm(request.POST)
        if form.is_valid() and optional_info_form.is_valid():

            email = form.cleaned_data.get('email')  # or email if you're using email as the username
            if User.objects.filter(username=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return render(request, 'createAccount.html', {'form': form})


            user = form.save(commit=False) 
            user.is_active = False  # User should not be active until they confirm their email
            # first_name = form.save(first_name)
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
            email = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')
            
            User = get_user_model()
            try:
                user = User.objects.get(email=email)  # Get the user based on the email
                user = authenticate(request, username=user.username, password=password)  # Authenticate with username
                if user is not None:
                    login(request, user)
                    return redirect('index')  # Redirect to a success page.
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password.'})
            except User.DoesNotExist:
                # No user was found, return invalid login error
                return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password.'})
    else:
        form = AuthenticationForm()  # Make sure to use your updated form
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
    
    
def search_movies(request):
    if request.method == 'GET':
        form = MovieSearchForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            movies = Movie.objects.filter(title__icontains=title)
            return render(request, 'search_results.html', {'movies': movies, 'form': form})
    else:
        form = MovieSearchForm()
    print(form)
    return render(request, 'search_movie.html', {'form': form})