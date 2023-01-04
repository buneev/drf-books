from .models import *
from .serializers import *
# from .filters import ChargeCardFilter
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.request import Request as drf_request
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter


class BookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'id']


