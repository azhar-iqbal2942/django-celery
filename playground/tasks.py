import random
import requests
from celery import shared_task


@shared_task()
def mail_chimp_subscribe(email):
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception("random processing error")

    print(f"Subscribing email {email}")
    # used for simulating a call to a third-party api
    requests.post("https://httpbin.org/delay/5")
