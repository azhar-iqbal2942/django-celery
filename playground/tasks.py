import time
from celery import shared_task


@shared_task()
def mail_chimp_subscribe(email):
    print(f"Subscribing email {email}")
    time.sleep(10)
