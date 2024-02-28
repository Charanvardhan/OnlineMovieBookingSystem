# forms.py

from django import forms

class MovieSearchForm(forms.Form):
    title = forms.CharField(label='Search by Title', max_length=100)
