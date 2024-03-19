from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.search_movies, name='search_movies'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile_view'), 
]
