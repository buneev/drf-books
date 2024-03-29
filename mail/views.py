import time
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from books.celery import app
from mail.tasks import *


class SleepView(APIView):

    def get(self, request):

        # sleep_task.delay()
        sleep_task.apply_async(args=[])

        return Response({
            'status': 'task created',
            'datetime': datetime.now()
        })

class SleepAndWaitAllTaskView(APIView):

    def get(self, request):

        tasks_result = []

        tasks_result.append(sleep_task.delay())
        tasks_result.append(sleep_task.apply_async(args=[]))
        result = app.send_task(
            'sleep_task_2',
            countdown=5, # not work (must be timeout)
            kwargs={'name': 'testname'}
        )
        tasks_result.append(result)

        # статус выполнения таски
        result.ready()

        while True:
            if all([t.ready() for t in tasks_result]):
                return Response({
                    'status': 'all tasks end',
                    'datetime': datetime.now()
                })
            else:
                time.sleep(1)

class SendMailView(APIView):
    """
    Отправка письма на почту.
    {
        "email": "buneev_ivan_r@mail.ru",
        "message": "test message"
    }
    """

    def post(self, request):

        email = request.data.get('email')
        message = request.data.get('message')

        # send_feedback_email_task.delay(email, message)
        send_feedback_email_task.apply_async(args=[email, message])

        return Response({
            'status': 'email send',
            'datetime': datetime.now()
        })

@api_view(['GET', 'POST'])
def async_upload_file_job(request):
    """
    Отправка файла в s3.
    {
        "local_file_path": "/Users/ivanbuneev/home/it/Kafka (основы).mp4",
        "s3_path": "celery-videos/Kafka (основы).mp4"
    }
    """

    if request.method == 'POST':
        local_file_path = request.data.get('local_file_path')
        s3_path = request.data.get('s3_path')
        if not all([local_file_path, s3_path]):
            return Response({'error': 'Параметр local_file_path, либо s3_path не был передан'})

        upload_file_task.apply_async(args=[local_file_path, s3_path], ignore_result=True)
        return Response({
            'status': 'start uploading file ...',
            'datetime': datetime.now()
        })
    return Response({})

