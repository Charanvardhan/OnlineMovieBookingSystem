from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

#url configuration
urlpatterns = [

    path('index/', views.index_view, name = 'index'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view), 
    path('createAccount/', views.create_account_view, name='createAccount'),
    path('registrationconfirmation/', views.registration_confirmation, name = 'registrationconfirmation')
]