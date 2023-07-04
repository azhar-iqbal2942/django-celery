import random
import requests
from celery import shared_task
from celery.signals import task_postrun

from .consumers import notify_channel_layer


@shared_task()
def mail_chimp_subscribe(email):
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception("random processing error")

    print(f"Subscribing email {email}")
    # used for simulating a call to a third-party api
    requests.post("https://httpbin.org/delay/5")


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    """
    When celery task finish, send notification to Django channel_layer, so Django channel would receive
    the event and then send it to web client
    """
    notify_channel_layer(task_id)
