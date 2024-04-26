from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from .views import filter_movies, show_movie_details

# app_name = "users"
#url configuration for users
urlpatterns = [



    path('index/', views.index_view, name = 'index'),
    path("index/<int:pk>/", show_movie_details, name = 'm_detail'),
    path('login/', views.login_view, name='login'),
    path('adminlogin/', views.admin_login_view, name='admin-login'),
    path('admin/', views.admin_redirect, name='admin_redirect'),
    path('adminHome/', views.admin_home_view, name='admin-home'),
    path('logout/', views.logout_view, name='log-out'),
    path('profile/', views.profile_view, name='profile'), 
    path('createAccount/', views.create_account_view, name='createAccount'),
    path('emailverification/', views.create_account_view, name = 'emailverification'),
    path('registrationconfirmation/', views.registration_confirmation, name = 'registrationconfirmation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path('change_password/', views.change_password, name='change_password'),
    path('search_movie/', views.filter_movies, name='search_movie'),
    path('add_movie/', views.add_movie, name='add-movie'),
    path('adminmovies/', views.manage_movies_view, name='manage-movies'),
    path('show/<int:pk>/', views.order_summary_view, name='show'),
    path('adminpromotions/', views.promotions_view, name='promotions'),
    path('adminusers/', views.admin_users_view, name='admin-users'),


    # path('show/<int:id>/', views.show, name='show')

    #path('adminlogin/')
]