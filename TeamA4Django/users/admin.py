from django.contrib import admin
from .models import UserProfile, CreditCard, Movie

admin.site.register(UserProfile)
admin.site.register(CreditCard)
admin.site.register(Movie)


# Register your models here.
