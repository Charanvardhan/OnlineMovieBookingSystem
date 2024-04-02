from django.contrib import admin
from .models import UserProfile, CreditCard, Movie, Customer, Bookings, Showtimes
from .models import Admin, Promotions, Show, TicketPrices, Showroom, Ticket

admin.site.register(UserProfile)
admin.site.register(CreditCard)
admin.site.register(Movie)
admin.site.register(Customer)
admin.site.register(Bookings)
admin.site.register(Showtimes)
admin.site.register(Admin)
admin.site.register(Promotions)
admin.site.register(Show)
admin.site.register(Ticket)
admin.site.register(TicketPrices)
admin.site.register(Showroom)




# Register your models here.
