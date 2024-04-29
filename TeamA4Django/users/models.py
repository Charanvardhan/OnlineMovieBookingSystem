from xml.dom import ValidationErr
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.forms import ValidationError
from django.utils import timezone
import uuid
from django.db import models
from django.core.exceptions import ValidationError
import datetime
from cryptography.fernet import Fernet
import os
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
##Difference between this and Customer??
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #need first, last name
    # Other fields remain unchanged
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
    card_number = models.CharField(max_length=255, blank=True)  
    expiration = models.CharField(max_length=5, blank=True)  
    cvv = models.CharField(max_length=255, blank=True)
    billing_zip_postal_code = models.CharField(max_length=12, blank=True)
    subscribe_to_promotions = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def first_and_last_name (self):
        return f"{self.first_name} {self.last_name}"
    
    def booking_history (self):
        return BookingHistory.objects.filter(user=self) 

    # def decrypt_card_info(self):
    #     if self.card_number and self.cvv:
    #         key = os.environ.get('FERNET_KEY')
    #         fernet = Fernet(key)
    #         x = self.card_number
    #         decrypted_card_number = fernet.decrypt(x).decode()
    #         decrypted_cvv = fernet.decrypt(x).decode()
    #         return decrypted_card_number, decrypted_cvv
    #     else:
    #         return None, None

    def save(self, *args, **kwargs):
        print("Arguments (*args):", args)
        print("Keyword arguments (**kwargs):", kwargs)
        if self.card_number:
            self.card_number = self.encrypt_data(self.card_number)
             # Clear the original card number after encryption
        if self.cvv:
            self.cvv = self.encrypt_data(self.cvv)
              # Clear the original CVV after encryption
        super().save(*args, **kwargs)

    def encrypt_data(self, data):
        key = settings.FERNET_KEY.encode()
        fernet = Fernet(key)
        return fernet.encrypt(data.encode())


class Status(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    INACTIVE = 'Inactive', 'Inactive'
    SUSPENDED = 'Suspended', 'Suspended'


##What is the difference between this and UserProfile???
# class Customer(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     status = models.CharField(
#         max_length=10,
#         choices=Status.choices,
#         default=Status.ACTIVE,
#     )

#     def storePaymentCard(self):
#         pass

#     def checkout(self):
#         pass
    
#     def booking_history (self):
#         return BookingHistory.objects.filter(user=self) 
    





#credit card model 
class CreditCard(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
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

    # def updateSeats(self):
    #     pass
   
    def __str__(self):
     return f"Credit Card for {self.user.first_name} {self.user.last_name}"


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
    show = models.CharField(max_length=100, null=True, blank=True) 
    is_available = models.BooleanField(default=False)

    def validatePromoCode(self):
        pass

    def status(self):
        pass
    


class TimeSlot(models.TextChoices):
    MORNING = 'Morning 09:00-12:00', '09:00-12:00'
    AFTERNOON = 'Afternoon 12:00-15:00', '12:00-15:00'
    EVENING = 'Evening 15:00-18:00', '15:00-18:00'
    NIGHT = 'Night 18:00-21:00', '18:00-21:00'

##Need var numSeats, fk to Seat
class Showroom(models.Model):
    seats1 = models.IntegerField()
    showroom_number = models.IntegerField(unique=True)

    def get_seats(self):
        return self.seats

    def __str__(self):
        return f"Showroom {self.showroom_number}"

#Need var numAvailSeats, all seats in ShowRoom
class Showtimes(models.Model):
    date = models.DateField(default=timezone.now)
    time_slot = models.CharField(max_length=40, choices=TimeSlot.choices, default=TimeSlot.MORNING)
    showroom = models.ForeignKey('Showroom', on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('date', 'time_slot', 'showroom')

    def get_formatted_showtimes(self):
        for choice in TimeSlot.choices:
            if choice[0] == self.time_slot:
                return f"{choice[0]} {choice[1]}"
        return ""

    def __str__(self):
        return self.get_formatted_showtimes()
    
class Bookings(models.Model):
    #customer_id = 
    #promotion_id =
    # show_id = models.IntegerField(unique=True)
    # (Having card id => which card user used to perform booking is also a good practice.)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.OneToOneField(Showtimes, on_delete=models.CASCADE)
    booking_number = models.IntegerField(unique=True)
    ticket_number = models.IntegerField()
    availability = models.IntegerField()

    def purchaseTicket(self):
        pass

    def deleteBooking(self):
        pass

class Show(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, default=1)
    showroom = models.ForeignKey('Showroom', on_delete=models.CASCADE, default=1)
    showtime = models.ForeignKey('Showtimes', on_delete=models.CASCADE, default=1)
    show_id = models.IntegerField(unique=True)
    #ticket = models.ManyToManyField('Ticket', default = 'true')

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Check if this is a new record
    #         self.assignShowtime(self.showtime.id)
    #     super().save(*args, **kwargs)

    # def assignShowtime(self, showtime_id):
    #     new_showtime = Showtimes.objects.get(id=showtime_id)
    #     conflicting_show = Show.objects.filter(
    #         showroom=new_showtime.showroom,
    #         showtime__date=new_showtime.date,
    #         showtime__time_slot=new_showtime.time_slot
    #     ).exclude(id=self.id).exists()  # Exclude self for updates

    #     if conflicting_show:
    #         raise ValidationError("This time slot in the selected showroom is already booked.")

    #     self.showtime = new_showtime

    def __str__(self):
        return f"{self.movie} at {self.showtime}"


#class TicketType1(models.Model):
     #name = models.CharField(max_length=100, default='Generic Ticket')
     #price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Price per ticket", default='0.00')


#class Ticket1(models.Model):
    # Ticket maps booking to the seat. 
    #The ticket price schema can be used as foreign key in tickets.
    # Also mention the type of ticket in ticket
    #ticket_number = models.AutoField(primary_key=True)  # Ensuring each ticket number is unique
    #ticket_type = models.ForeignKey(TicketType1, on_delete=models.CASCADE, null=True)
    #quantity = models.IntegerField(default=0)


class BookingHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='booking_histories', default = 1)
    # Add fields to store booking details like booking number, ticket number, etc.
    booking_number = models.IntegerField(unique=True)
    ticket_number = models.IntegerField()
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    #show = models.ForeignKey
        # Add other fields as needed

    def display_booking_info(self):
        return f"Booking Number: {self.booking_number}, Ticket Number: {self.ticket_number}"
    
class Seat(models.Model):
    showroom = models.ForeignKey('Showroom', on_delete=models.CASCADE, related_name='seats')
    row = models.IntegerField()
    column = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Row {self.row}, Seat {self.column} in Showroom {self.showroom.showroom_number}"
