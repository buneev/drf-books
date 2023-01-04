from django.db.transaction import atomic
from rest_framework import serializers
from .models import *
from datetime import datetime, timezone
# from .enums import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

