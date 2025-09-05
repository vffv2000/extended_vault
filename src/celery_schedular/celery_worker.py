"""Celery worker configuration for task scheduling and execution."""

from celery import Celery

from src.core.config import settings

celery = Celery(
    "task_scheduler",
    broker=settings.broker_for_rabbitmq,
    backend="rpc://",
    include=["src.celery_schedular.tasks"],
)

celery.conf.beat_schedule = {
    "test-task-print-unix-time": {
        "task": "src.celery_schedular.tasks.print_unix",
        "schedule": 3600,
    }

}
celery.conf.worker_concurrency = 1
celery.conf.timezone = "UTC"
celery.conf.beat_scheduler = "celery.beat:PersistentScheduler"
