from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.utils import timezone




#To-DO
#Showroom, show, showtime and booking

#User profile is redundant.
#  Keep credit card details in credit card.
#  User details in customer. 
#  And then in credit card, give the customer id instead of user_profile id

#class User(AbstractUser):
    # Inherits from Django's AbstractUser
 #   pass

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


class Status(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    INACTIVE = 'Inactive', 'Inactive'
    SUSPENDED = 'Suspended', 'Suspended'

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def storePaymentCard(self):
        pass

    def checkout(self):
        pass


#credit card model 
class CreditCard(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
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

    def validate(self):
        pass

    def addPayment(self):
        pass

    def updateSeats(self):
        pass
   
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
    title = models.CharField(max_length=100, unique = True) #cant be a CharField
    description = models.TextField(max_length=200, default='None')
    cast = models.TextField(max_length=100, default='None')
    producer = models.TextField(max_length=100, default='None')
    director = models.TextField(max_length=100, default='None')
    review = models.TextField(max_length=200, default='None')
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes, helpful for scheduling
    trailer_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='static/assets/img/gallery', null=True, blank=True) 
    # image = models.URLField(max_length = 200, default = 'none')
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default='none')
    rating = models.CharField(max_length=100, choices=RATING, default='none')
    status = models.CharField(max_length=100, choices=STATUS, default='nowPlaying')
    # isPlaying = models.BooleanField
    def __str__(self):
        return f"{self.title}"
    
    ## define YoutubeProxy function

    ##define API
    #Note: Movie missing cast information (good to have)



class Bookings(models.Model):
    #customer_id = 
    #promotion_id =
    # show_id = models.IntegerField(unique=True)
    # (Having card id => which card user used to perform booking is also a good practice.)
    booking_number = models.IntegerField(unique=True)
    ticket_number = models.IntegerField()
    availability = models.IntegerField()

    def purchaseTicket(self):
        pass

    def deleteBooking(self):
        pass


class Ticket(models.Model):
    # Ticket maps booking to the seat. 
    #The ticket price schema can be used as foreign key in tickets.
    # Also mention the type of ticket in ticket
    ticket_number = models.IntegerField() #idk if this should be here, added to remove error 



class Showtimes(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def updateShowtimes(self):
        pass

    def seatSelection(self):
        pass

class Admin(models.Model):
    user_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def manageMovies(self):
        pass

    def manageUsers(self):
        pass

class Promotions(models.Model):
    code = models.CharField(max_length=100, unique=True)
    percentage = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    show = models.CharField(max_length=100)
    is_available = models.BooleanField(default=False)

    def validatePromoCode(self):
        pass

    def status(self):
        pass

class Show(models.Model):
    #showtime (use foreign key)
    show_id = models.IntegerField(unique=True)
    date = models.DateField()
    duration = models.IntegerField()

    def assignShowtime(self):
        pass

    def assignShowroom(self):
        pass

class TicketPrices(models.Model):
    adult_tickets = models.IntegerField()
    senior_tickets = models.IntegerField()
    child_tickets = models.IntegerField()

    def applyPromotion(self):
        pass

    def applyShowtime(self):
        pass

class Showroom(models.Model):
    seats = models.IntegerField()
    showroom_number = models.IntegerField(unique=True)

    def updateMovieShowing(self):
        pass

    def retrieveSeats(self):
        pass
    

##Showtimes model 
#does scheduling, 
    ##Movie will a fk to showtime, if its now palying
    
    

#Booking model 
    #fk to user, 
    #tickets
    #fk to showing (need class show)

