import random
import requests
import celery
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger

from .consumers import notify_channel_layer

logger = get_task_logger(__name__)


class BaseTaskWithRetry(celery.Task):
    """
    Base celery configurations
    """

    autoretry_for = (Exception, KeyError)
    retry_kwargs = {"max_retries": 5}
    retry_backoff = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def mail_chimp_subscribe(self, email):
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception("random processing error")

    print(f"Subscribing email {email}")
    # used for simulating a call to a third-party api
    requests.post("https://httpbin.org/delay/5")


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    """
    When celery task finish, send notification to Django channel_layer, so Django
    channel would receive the event and then send it to web client.
    """
    notify_channel_layer(task_id)


# Note: task name must be unique throughout the app.
@shared_task(name="task_clear_session")
def task_clear_session():
    from django.core.management import call_command

    call_command("clearsessions")


@shared_task(name="default:dynamic_example_one")
def dynamic_example_one():
    logger.info("Example One")


@shared_task(name="low_priority:dynamic_example_two")
def dynamic_example_two():
    logger.info("Example Two")


@shared_task(name="high_priority:dynamic_example_three")
def dynamic_example_three():
    logger.info("Example Three")
