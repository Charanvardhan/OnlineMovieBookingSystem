# forms.py

from django import forms

class MovieSearchForm(forms.Form):
    title = forms.CharField(label='Search by Title', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())