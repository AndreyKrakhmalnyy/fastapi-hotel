from time import sleep
from app.tasks.celery import celery_instance


@celery_instance.task
def test_task():
    sleep(5)
    print("END")
