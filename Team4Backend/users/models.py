from django.db import models
from django.contrib.auth.models import AbstractUser
from abc import ABC, abstractmethod
from enum import Enum

class Status(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'


##Ask about clashes... I'm trying to make User an interface that Customer and Admin both inherit from. 
    #A button click on User will call the constructor of Customer. (right?)
class User(AbstractUser):
    # Add any common fields or methods for both Customer and Admin here
    #emailConfirmed: whether or not the user has verified their email
    email_confirmed = models.BooleanField(default=False)
    user_id = models.CharField(max_length=50)

    class Meta:
        abstract = True

    #verifyUser()
    pass

class Customer(User):
    # Add any customer-specific fields or methods here
    # Additional instance variables for Customer
    
    is_subscribed = models.BooleanField(default=False)


    #This will pull from the front end, 
    #will assign the instance variables: email, first name, last name, password, isSubscribed, creditCard
    #Automatically sets the status to Inactive
    #Calls the send verificationEmail
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default status for Customer
        self.status = Status.INACTIVE.value
    pass

class Admin(User):
    # Add any admin-specific fields or methods here

    #Methods

    #ManageUser(): accesses the Customer database and ...

    #ManageMovies(): access and edit the Movies database.
    pass

# Create your models here.
