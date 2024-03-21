from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm  # I'm assuming you created this based on previous messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse


def create_account_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('registrationconfirmation')  
        else: 
            print(form.errors)  # Debug print
    else:
        form = CustomUserCreationForm()

    return render(request, "createAccount.html", {"form": form})

def index_view(request):
   return render(request, 'index.html')

def profile_view(request):
   return render(request, 'profile.html')

def login_view(request):
    # Assuming you want to use the AuthenticationForm for logging in
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to a success page.
            else:
                # Return an 'invalid login' error message.
                pass  # You can add a message or do something else here
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registration_confirmation(request):
    return render(request, 'registrationconfirmation.html')