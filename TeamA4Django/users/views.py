from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomLoginForm
from django.http import HttpResponse

def index_view(request):
   return render(request, 'index.html')

def profile_view(request):
   return render(request, 'profile.html')

def login_view(request):
    return render(request, 'login.html')

# Create your views (request handlers) here.
