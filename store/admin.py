from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *


@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass
