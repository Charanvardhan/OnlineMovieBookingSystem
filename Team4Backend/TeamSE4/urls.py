from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('search/', views.search_movies, name='search_movies'),
]