from django_filters import rest_framework
from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(lookup_expr='contains')
    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(lookup_expr='slug')

    class Meta:
        model = Title
        fields = ('year',)
