from random import randint
from time import sleep
from django.core.mail import send_mail
from celery import shared_task


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

@shared_task()
def sleep_task():
    sleep_sec = randint(20, 40)
    sleep(sleep_sec)
    return {'sleep_sec': sleep_sec}

