"""Celery tasks for periodic operations."""
import asyncio
import time
from celery import shared_task


from core.custom_logs import log


@shared_task
def print_unix():
    """Celery task to print the current UNIX time."""
    ts = int(time.time())
    log.info(f"[TASK] Current UNIX time: {ts}")

