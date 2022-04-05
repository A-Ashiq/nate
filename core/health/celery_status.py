"""
This module holds functionality for checking the status of Celery
"""
from celery import Celery

from celery_app import celery


def celery_worker_is_healthy(celery_app: Celery = None, timeout: int = 1) -> bool:
    """
    Checks if the celery worker is available by checking the queue.

    Returns:
        (bool) - True if the celery worker is available, False otherwise.

    """
    if celery_app is None:
        celery_app = celery

    try:
        celery_status_results = celery_app.control.inspect(timeout=timeout).active_queues()
    except Exception:
        return False

    return celery_status_results is not None
