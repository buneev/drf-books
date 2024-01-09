from django.contrib import admin
from django.contrib.admin import ModelAdmin
from store.models import *


@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass


@admin.register(UserBookRelation)
class UserBookRelationAsmin(ModelAdmin):
    pass

