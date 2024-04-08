from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


#user profile model and fields
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #username/id
    #need first, last name
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100, null=True, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    apartment_suite = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_province = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    zip_postal_code = models.CharField(max_length=12, blank=True)
    name_on_card = models.CharField(max_length=100, blank=True)
    card_number = models.CharField(max_length=16, blank=True)  
    expiration = models.CharField(max_length=5, blank=True)  
    cvv = models.CharField(max_length=4, blank=True)
    billing_zip_postal_code = models.CharField(max_length=12, blank=True)
    subscribe_to_promotions = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"


#credit card model 
class CreditCard(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name_on_card = models.CharField(max_length=100, blank=True)  
    card_number = models.CharField(max_length=16, blank=True)
    cvv = models.CharField(max_length=4,blank=True)
    expiration = models.CharField(max_length=5, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    apartment_suite = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_province = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    zip_postal_code = models.CharField(max_length=12, blank=True)
   

    def __str__(self):
        return f"Credit Card for {self.user_profile.user.username}"

#movie card model
#movie title, category, cast, director, producer, synopsis, reviews, trailer picture and video
#MPAA-US film rating code [1], and show dates and times (done in showtimes, not Bookings)
class Movie(models.Model):
    GENRE_CHOICES = [
        ('none', 'None'), 
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('sci-fi', 'Science Fiction'),
    ]
    RATING = [
        ('none', 'None'), 
        ('g', 'G'),
        ('pg', 'PG'),
        ('pg13', 'PG13'),
        ('r', 'R')
    ]
    STATUS = [
        ('nowPlaying', 'Now Playing'),
        ('comingSoon', 'Coming Soon')
    ]
    title = models.CharField(max_length=100, unique = True)
    description = models.TextField(max_length=100, default='None')
    cast = models.TextField(max_length=100, default='None')
    producer = models.TextField(max_length=100, default='None')
    director = models.TextField(max_length=100, default='None')
    review = models.TextField(max_length=100, default='None')
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes, helpful for scheduling
    trailer_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='movie_images/', null=True, blank=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default='none')
    rating = models.CharField(max_length=100, choices=RATING, default='none')
    status = models.CharField(max_length=100, choices=STATUS, default='nowPlaying')
    # isPlaying = models.BooleanField
    def __str__(self):
        return f"{self.title}"
# Create your models here.
    

##Showtimes model 
#does scheduling, 
    
    

#Booking model 
    #fk to user, 
    #tickets
    #fk to showing (need class show)