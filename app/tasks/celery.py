from celery import Celery
from app.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "app.tasks.tasks",
    ],
)

celery_instance.conf.beat_schedule = {
    "bookings_message": {
        "task": "booking_today_alert",
        "schedule": 5,
    }
}
