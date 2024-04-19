from xml.dom import ValidationErr
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.forms import ValidationError
from django.utils import timezone
import uuid




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
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    trailer_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='movie_images/', null=True, blank=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default='none')
    
    def __str__(self):
        return self.title   
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
    
    
from django.db import models
from django.core.exceptions import ValidationError
import datetime

class TimeSlot(models.TextChoices):
    MORNING = 'Morning', '09:00-12:00'
    AFTERNOON = 'Afternoon', '12:00-15:00'
    EVENING = 'Evening', '15:00-18:00'
    NIGHT = 'Night', '18:00-21:00'

class Showroom(models.Model):
    seats = models.IntegerField()
    showroom_number = models.IntegerField(unique=True)

    def get_seats(self):
        return self.seats

    def __str__(self):
        return f"Showroom {self.showroom_number}"

class Showtimes(models.Model):
    date = models.DateField(default=timezone.now)
    time_slot = models.CharField(max_length=15, choices=TimeSlot.choices, default=TimeSlot.MORNING)
    showroom = models.ForeignKey('Showroom', on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('date', 'time_slot', 'showroom')

    def get_formatted_showtimes(self):
        time_range = TimeSlot.labels[TimeSlot.values.index(self.time_slot)]
        return f"{self.date} {time_range}"

    def __str__(self):
        return self.get_formatted_showtimes()

class Show(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, default=1)
    showroom = models.ForeignKey('Showroom', on_delete=models.CASCADE, default=1)
    showtime = models.ForeignKey('Showtimes', on_delete=models.CASCADE, default=1)
    show_id = models.IntegerField(unique=True)

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



class TicketPrices(models.Model):
    adult_tickets = models.IntegerField()
    senior_tickets = models.IntegerField()
    child_tickets = models.IntegerField()

    def applyPromotion(self):
        pass

    def applyShowtime(self):
        pass


