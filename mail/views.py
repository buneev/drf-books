from datetime import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from mail.tasks import *

class SendMailView(APIView):
    """
    {
        "email": "buneev_ivan_r@mail.ru",
        "message": "test message"
    }
    """

    def post(self, request):
        email = request.data.get('email')
        message = request.data.get('message')
        send_feedback_email_task.delay(email, message)
        return Response({'status': 'task created'})

class SleepView(APIView):

    def get(self, request):

        # sleep_task.delay()
        sleep_task.apply_async(args=[])

        return Response({
            'status': 'task created',
            'datetime': datetime.now()
        })
