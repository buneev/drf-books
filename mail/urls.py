from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "article"

urlpatterns = [
    path('send/', SendMailView.as_view()),
    path('sleep/', SleepView.as_view()),
]

