from base64 import urlsafe_b64encode
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import OptionalInfoForm, CustomUserCreationForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
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
import base64
from Crypto.Cipher import AES
from django.conf import settings
from .models import UserProfile
from .models import Movie, UserProfile, CreditCard
from .forms import MovieSearchForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordResetForm, UserProfileForm, CreditCardForm, UserProfileEditForm
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


def encrypt_card_info(card_number, cvv):
    # Pad card_number and cvv to 16 bytes if needed
    card_number = card_number.ljust(16)[:16]
    cvv = cvv.ljust(4)[:4]

    # Encode card_number and cvv
    card_number_bytes = card_number.encode()
    cvv_bytes = cvv.encode()
    secret_key_bytes = settings.SECRET_KEY.encode()
    # Encrypt card information using AES encryption
    cipher = AES.new(secret_key_bytes[:32], AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(card_number_bytes + cvv_bytes)

    # Return base64 encoded ciphertext and tag
    return base64.b64encode(ciphertext).decode(), base64.b64encode(tag).decode()


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
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        # Check if the form is valid:
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin-home')  
                else:
                    messages.error(request, 'Login failed: You are not an admin.')
            else:
                messages.error(request, 'Login failed: Invalid username or password.')
        else:
            messages.error(request, 'Login failed: Invalid form input.')
    else:
        form = AuthenticationForm()

    return render(request, 'admin/adminlogin.html', {'form': form})

   

def admin_home_view(request):
     return render(request, 'adminHome.html')


def create_account_view(request):
    user_profile_form = UserProfileForm(request.POST or None)
    credit_card_form = CreditCardForm(request.POST or None)

    if request.method == 'POST':
        if user_profile_form.is_valid():
            user = User.objects.create_user(
                username=user_profile_form.cleaned_data['email'],
                email=user_profile_form.cleaned_data['email'],
                is_active=False 
            )

            password = request.POST['password1']
            user.set_password(password)
            user.save()
            user_profile = UserProfile(user=user, **user_profile_form.cleaned_data)
            user_profile.save()

            if credit_card_form.is_valid():
                credit_card = credit_card_form.save(commit=False)
                credit_card.user_profile = user_profile
                credit_card.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your SINABOOK account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_b64encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = user_profile_form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.success(request, 'Please confirm your email address to complete the registration.')
                return redirect('login')  
            else:
                messages.error(request, 'Please correct the error in the credit card information.')
        else:
            messages.error(request, 'Please correct the error in the user profile information.')

    return render(request, 'createAccount.html', {
        'user_profile_form': user_profile_form,
        'credit_card_form': credit_card_form
    })

def safe_b64decode(data):
    """Attempt to base64 decode with padding adjustments."""
    try:
        return base64.b64decode(data)
    except Exception as e:
        # Adjust padding and retry
        padding = 4 - (len(data) % 4)
        data += "=" * padding
        try:
            return base64.b64decode(data)
        except Exception as e:
            print(f"Failed to decode: {e}")
            return None
          
def decrypt_card_info(encrypted_data):
    secret_key_bytes = settings.SECRET_KEY.encode()[:32]
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    nonce, ciphertext_tag = encrypted_data_bytes[:16], encrypted_data_bytes[16:]
    
    cipher = AES.new(secret_key_bytes, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt(ciphertext_tag[:-16])

    try:
        cipher.verify(ciphertext_tag[-16:])
        #decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        # Split the decrypted data into card_number and cvv
        card_number = decrypted_data[:16].decode().strip()
        cvv = decrypted_data[16:].decode().strip()
        return card_number, cvv
    except ValueError as e:
        # Decryption failed
        print("Decryption error:", str(e))
        return None, None
 
    
def index_view(request):
   return render(request, 'index.html')

#The instance of the user is displayed on profile.html with email being an uneditable field
#I cannot check when user is logged out
@login_required
def profile_view(request):
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    decrypted_card_number, decrypted_cvv = decrypt_card_info(user_profile.card_number)

    if 'submit_user_form' in request.POST:
        #use userprofile edit form 
        user_form = UserProfileEditForm(request.POST, instance=user_profile, prefix='user')
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=user_profile, prefix='user')
    
    if 'submit_password_form' in request.POST:
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(user)
    
    # Assuming a OneToOne relationship with CreditCard for simplicity
    try:
     credit_card = CreditCard.objects.filter(user_profile=user_profile).first()
    except CreditCard.DoesNotExist:
     credit_card = None
    
    if 'submit_credit_card_form' in request.POST and credit_card:
        credit_card_form = CreditCardForm(request.POST, instance=credit_card, prefix='credit')
        if credit_card_form.is_valid():
            credit_card_form.save()
            messages.success(request, 'Your credit card information has been updated successfully!')
            return redirect('profile')
    else:
        credit_card_form = CreditCardForm(instance=credit_card, prefix='credit') if credit_card else None
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'password_form': password_form,
        'credit_card_form': credit_card_form,
        'decrypted_card_number': decrypted_card_number,
        'decrypted_cvv': decrypted_cvv
    })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            email = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')
            
            User = get_user_model()
            try:
                user = User.objects.get(email=email) 
                user = authenticate(request, username=user.username, password=password)  
                if user is not None:
                    login(request, user)
                    return redirect('index')  
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password.'})
            except User.DoesNotExist:
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
    

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changePwd.html', {
        'form': form
    })
    
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