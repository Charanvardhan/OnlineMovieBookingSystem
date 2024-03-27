from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

#url configuration
urlpatterns = [


    path('index/', views.index_view, name = 'index'),
    path('login/', views.login_view, name='login'),
    path('adminlogin/', views.admin_login_view, name='admin-login'),
    path('adminHome/', views.admin_home_view, name='admin-home'),
    path('logout/', views.logout_view, name='log-out'),
    path('profile/', views.profile_view, name='profile'), 
    path('createAccount/', views.create_account_view, name='createAccount'),
    path('registrationconfirmation/', views.registration_confirmation, name = 'registrationconfirmation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path('search/', views.search_movies, name='search_movies'),

    #path('adminlogin/')
]