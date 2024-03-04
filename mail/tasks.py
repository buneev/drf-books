from random import randint
from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from books.celery import app
from .s3client import *
import logging

logger = logging.getLogger(__name__)


@shared_task()
def sleep_task():
    sleep_sec = randint(5, 15)
    sleep(sleep_sec)
    logger.info("task 'sleep_task' was completed")
    return {'sleep_sec': sleep_sec}


@app.task(name='sleep_task_2')
def sleep_task_2(name):
    sleep_sec = randint(5, 15)
    sleep(sleep_sec)
    x = 1 / 0
    logger.info("task 'sleep_task_2' was completed")
    return {'sleep_sec': sleep_sec}


@shared_task()
def send_feedback_email_task(email_address, message):
    """Sends an email when the feedback form has been submitted."""

    sleep(10)
    send_mail(
        "Your Feedback",
        f"\t{message}\n\nThank you!",
        "buneev_ivan_r@mail.ru",
        [email_address],
        fail_silently=False,
    )
    logger.info("task 'send_feedback_email_task' was completed")


@shared_task()
def upload_file_task(local_path, path):
    upload_file_to_s3(local_path, path)
    logger.info("task 'upload_file_task' was completed")
    return 'success'
