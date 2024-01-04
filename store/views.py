from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from store.filters import BookFilter
from store.models import Book
from store.serializers import BookSerializer


class BookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    # filterset_fields = ['name', 'price']
    search_fields = ['name', 'price']
    ordering_fields = ['id', 'name', 'price']
