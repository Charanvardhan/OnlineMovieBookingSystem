from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

#url configuration
urlpatterns = [
    path('index/', views.index_view),
    path('login/', views.login_view), 
    path('profile/', views.profile_view), 

]