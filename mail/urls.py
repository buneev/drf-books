from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "article"

urlpatterns = [
    path('send/', SendMailView.as_view()),
    path('sleep/', SleepView.as_view()),
    path('sleep_and_wait_all_tasks/', SleepAndWaitAllTaskView.as_view()),
    path('upload_file/', async_upload_file_job, name='async_upload_file_job')
]

