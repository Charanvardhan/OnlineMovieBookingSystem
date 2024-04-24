import django_filters
from .models import Movie

class MovieFilter (django_filters.FilterSet):
    # title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Movie
        fields = {"title": ["iexact"],
                   "genre": ["icontains"],
                #    "showtimes": ["exact", "year__gt"]
                } #add showtimes later
                  