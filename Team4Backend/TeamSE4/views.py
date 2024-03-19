from datetime import datetime
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from .models import Movie

from django.shortcuts import render
from .models import Movie
from .forms import MovieSearchForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    return render(request, 'blog/post_list.html', {})

def home(request):
    now_showing_movies = Movie.objects.filter(release_date__lte=datetime.now())
    coming_soon_movies = Movie.objects.filter(release_date__gt=datetime.now())
    print(now_showing_movies)
    return render(request, 'html/index.html', {'now_showing_movies': now_showing_movies, 'coming_soon_movies': coming_soon_movies})


def search_movies(request):
    if request.method == 'GET':
        form = MovieSearchForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            movies = Movie.objects.filter(title__icontains=title)
            return render(request, 'search_results.html', {'movies': movies, 'form': form})
    else:
        form = MovieSearchForm()
    print(form)
    return render(request, 'search_movies.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def profile_view(request):
    return render(request, 'profile.html') 


