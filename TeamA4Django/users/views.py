from base64 import urlsafe_b64encode
import json
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from .forms import OptionalInfoForm, CustomUserCreationForm, EditProfileForm, PromotionsForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.core.serializers import serialize
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from dateutil import parser
import datetime
import base64
from Crypto.Cipher import AES
from django.conf import settings
from .models import UserProfile, Promotions
from .models import Movie, UserProfile, CreditCard, Show, Showtimes
from .forms import MovieSearchForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordResetForm, UserProfileForm, CreditCardForm, UserProfileEditForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import MovieForm
# from flask import Flask, render_template
from django.core.management import call_command
import django_filters
from .filters import MovieFilter
from django.db.models.signals import post_save
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models import Q


from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db.models.signals import post_save
from django.dispatch import receiver


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

##do login check not here, but in index.html!
def home_view(request):
    movies = Movie.objects.all()
    
    context = {"movies": movies}
    return render(request, 'index.html', context)

def logout_view(request):
    logout(request) 
    return render(request, 'index.html')


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
                   login(request, user)  # Log in the user
                   messages.error(request, 'Access Denied: You are not an admin.')
                   return redirect('index')  # Redirect to a non-admin page
            else:
                messages.error(request, 'Login failed: Invalid username or password.')
        else:
            messages.error(request, 'Login failed: Invalid form input.')
    else:
        form = AuthenticationForm()

    return render(request, 'admin/adminlogin.html', {'form': form})

   
# Helper function to check if user is an admin
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required(login_url='/login/')  # Redirects to login page if not logged in
@user_passes_test(is_admin, login_url='/login/', redirect_field_name=None)
def admin_home_view(request):
    return render(request, 'adminHome.html')

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
                return redirect('emailverification')  
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
          
# def decrypt_card_info(encrypted_data):
#     secret_key_bytes = settings.SECRET_KEY.encode()[:32]
#     encrypted_data_bytes = base64.b64decode(encrypted_data)
#     nonce, ciphertext_tag = encrypted_data_bytes[:16], encrypted_data_bytes[16:]
    
#     cipher = AES.new(secret_key_bytes, AES.MODE_EAX, nonce=nonce)
#     decrypted_data = cipher.decrypt(ciphertext_tag[:-16])

#     try:
#         cipher.verify(ciphertext_tag[-16:])
#         #decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
#         # Split the decrypted data into card_number and cvv
#         card_number = decrypted_data[:16].decode().strip()
#         cvv = decrypted_data[16:].decode().strip()
#         return card_number, cvv
#     except ValueError as e:
#         # Decryption failed
#         print("Decryption error:", str(e))
#         return None, None
 

#Home Page
        #if user is logged in, displays the now playing and coming soon movies
        #if not logged in, go to login page
        #have seperate row for movies of status.nowPlaying and status.ComingSoon 
# @login_required    
        ##do login check
def index_view(request):
   # Call the management command
    # now_playing = call_command('populate_running_movies') ##This prepopulates the db for the first time, the index.html will need to refer to the db not this file
    # coming_soon = call_command('populate_coming_soon_movies')
    # print("Coming Soon : ", coming_soon[0].title)
    movies = Movie.objects.all()
    
    context = {"movies": movies}
    return render(request, 'index.html', context )
    # now_playing_movies = Movie.objects.filter(status='nowPlaying')
    # print("Now Playing : ", now_playing_movies[0].title)
    # coming_soon_movies = Movie.objects.filter(status='comingSoon')
    # print("Coming Soon : ", coming_soon_movies[0].title)

#This function shows Title, Description, Trailer, Cast, etc of a movie
#It is called when 'View Details' is clicked. 
def show_movie_details(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {"movie": movie}
    return render(request, 'm_detail.html', context)





#The instance of the user is displayed on profile.html with email being an uneditable field
#I cannot check when user is logged out
@login_required
def profile_view(request):
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    # decrypted_card_number, decrypted_cvv = decrypt_card_info(user_profile.card_number)

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
    
    try:
     credit_card = CreditCard.objects.filter(user_profile=user_profile).first()
     #credit_card = CreditCard.objects.filter(customer=user_profile.customer).first()

     

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
        # 'decrypted_card_number': decrypted_card_number,
        # 'decrypted_cvv': decrypted_cvv
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
    
##This takes input from the search bar, searches the movie database, and returns the movie that matches    
def search_movies(request):
    ##Changed from 'GET' to POST
    if request.method == 'POST':
        form = MovieSearchForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            movies = Movie.objects.filter(title__icontains=title)
            return render(request, 'search_results.html', {'movies': movies, 'form': form})
    else:
        form = MovieSearchForm()
    print(form)
    return render(request, 'search_movie.html', {'form': form})

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-home')  # Redirect to the movie list page or another appropriate page
    else:
        form = MovieForm()

    return render(request, 'add_movie.html', {'form': form})

@login_required(login_url='/login/')  # Redirects to login if not logged in
@user_passes_test(is_admin, login_url='/unauthorized/')  # Redirect if not admin
def manage_movies_view(request):
    movies = Movie.objects.all()  # Fetch all movies from the database
    return render(request, 'adminmovies.html', {'movies': movies})  


def unauthorized_view(request):
    return render(request, 'unauthorized.html')

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-home')  # Redirect to the movie list page or another appropriate page
    else:
        form = MovieForm()

    return render(request, 'add_movie.html', {'form': form})

@login_required(login_url='/login/')  # Redirects to login if not logged in
@user_passes_test(is_admin, login_url='/unauthorized/')  # Redirect if not admin
def manage_movies_view(request):
    movies = Movie.objects.all()  # Fetch all movies from the database
    return render(request, 'adminmovies.html', {'movies': movies})  


def unauthorized_view(request):
    return render(request, 'unauthorized.html')


##Current
def filter_movies(request):
    query = request.GET.get('q')
    print("Received query parameter:", query)  # Add this line to print the received query parameter
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query) | Q(genre__icontains=query))
    else:
        movies = Movie.objects.none()  # Return an empty queryset if no query is provided

    # movies_filter = MovieFilter(request.GET, queryset=Movie.objects.all())
    # movies = movies_filter.qs  # Access the filtered queryset
    print("in filter_movies, query was: ", query)
    print("the filtered movies are: ", movies)
        

    context = {
        'movies': movies,
        'query': query  # Pass the query to the template for display
    }
    
    print("SQL query:", movies.query)

    # if query:
    #     movies = Movie.objects.filter(title__icontains=query)
    #     # You can also filter by genre, rating, etc. as needed
    # else:
    #     movies = None
    return render(request, 'search_movie.html', context)


def show(request, id):
    if not id:
        return JsonResponse({'error': 'Show ID not provided'}, status=400)

    try:
        shows = Show.objects.select_related('showtime', 'showroom').filter(movie_id=id)
        
        if not shows.exists():
            return JsonResponse({'error': 'No shows found for this movie'}, status=404)

        show_data = []
        for show in shows:
            show_data.append({
                'show_id': show.show_id,
                'movie_id': show.movie.id,
                'showroom_number': show.showroom.showroom_number,
                'seats': show.showroom.get_seats(),
                'dates': show.showtime.date,
                'start_time': show.showtime.time_slot,
                # 'end_time': show.showtime.end_time,
            })
        
        return render(request, 'showBooking.html', {'shows': show_data})
    except Exception as e:
        print("hello")
        return JsonResponse({'error': str(e)}, status=500)


    

    
    
 
@receiver(post_save, sender=Promotions)
def send_promotion_email(sender, instance, created, **kwargs):
    if created and instance.is_available:
        subject = "New Promotion Available!"
        message = f"Hello! A new promotion with code {instance.code} is now available. Enjoy discounts on your next purchase!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in UserProfile.objects.filter(subscribe_to_promotions=True)]
        
        # Send email to all subscribed users
        send_mail(subject, message, from_email, recipient_list)   
        
        
def order_summary_view(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {"movie": movie}
    return render(request, 'orderSummary.html', context)

def promotions_view(request):
     if request.method == 'POST':
        form = PromotionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-home') 
     else:
        form = PromotionsForm()
     return render(request, 'adminpromotions.html', {'form': form})
    
def admin_users_view(request):

     return render(request, 'adminusers.html')   


def admin_redirect(request):
    return redirect('/admin/')