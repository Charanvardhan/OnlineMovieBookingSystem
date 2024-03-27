from django.conf import settings
from django.db import models

## Starting code

# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #username/id
#     #need first, last name
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     address_line_1 = models.CharField(max_length=255, blank=True)
#     address_line_2 = models.CharField(max_length=255, blank=True)
#     apartment_suite = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     state_province = models.CharField(max_length=100, blank=True)
#     country = models.CharField(max_length=50, blank=True)
#     zip_postal_code = models.CharField(max_length=12, blank=True)
#     name_on_card = models.CharField(max_length=100, blank=True)
#     card_number = models.CharField(max_length=16, blank=True)  
#     expiration = models.CharField(max_length=5, blank=True)  
#     cvv = models.CharField(max_length=4, blank=True)
#     billing_zip_postal_code = models.CharField(max_length=12, blank=True)
#     subscribe_to_promotions = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.username}'s profile"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #username/id
    #need first, last name
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
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



class CreditCard(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=4)
    expiration = models.CharField(max_length=5, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    apartment_suite = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_province = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    zip_postal_code = models.CharField(max_length=12, blank=True)
    name_on_card = models.CharField(max_length=100, blank=True)  

    def __str__(self):
        return f"Credit Card for {self.user_profile.user.username}"