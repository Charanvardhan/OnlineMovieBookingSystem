import django_filters
from .models import Movie

class MovieFilter (django_filters.FilterSet):
    # title = django_filters.CharFilter(lookup_expr='iexact')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['title', 'genre']
                  