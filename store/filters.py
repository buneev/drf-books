from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


class BookFilter(filters.FilterSet):
    ids = filters.BaseInFilter(field_name='id')
    price = filters.CharFilter(
        field_name="price", lookup_expr="icontains"
    )
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )
