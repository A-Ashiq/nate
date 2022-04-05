"""
This module holds functionality for parsing statuses of services throughout the platform
"""

from typing import Callable, Dict

from core.health.celery_status import celery_worker_is_healthy
from core.health.postgres_status import postgres_is_healthy


def parse_health_boolean(bool: bool) -> str:
    """
    Stringifies a boolean into a more end-user friendly value

    Args:
        bool: An input boolean value to be converted

    Returns:
        (str) - "HEALTHY" if `bool` is Truthy, "UNHEALTHY" otheriwse

    """
    return "HEALTHY" if bool else "UNHEALTHY"


def get_health_statuses(
    celery_health_checker: Callable = celery_worker_is_healthy,
    postgres_health_checker: Callable = postgres_is_healthy,
    status_parser: Callable = parse_health_boolean,
) -> Dict[str, str]:
    """
    Gets the health statuses of services within the application.

    The callable passed to `status_parser` can be used to customise the status output.
    Currently this defaults to the following:
        - "HEALTHY": If the service responded to the probe.
        - "UNHEALTHY": If the service did not respond to the probe.

    Example return value:

        {"service_a": "HEALTHY", "service_b": "UNHEALTHY"}

    Args:
        celery_health_checker: Callable used to determine the health of celery.
            Defaults to `celery_worker_is_healthy()`.
        postgres_health_checker: Callable used to determine the health of postgres.
            Defaults to `postgres_is_healthy()`.
        status_parser: Callable used to determine the output of a given health status.
            Defaults to `parse_health_boolean()`.

    Returns:
        (dict) - Keys being the service name, and the value being the health status.

    """
    celery_is_ready = celery_health_checker()
    postgres_is_ready = postgres_health_checker()

    return {
        "celery": status_parser(celery_is_ready),
        "postgres": status_parser(postgres_is_ready),
    }
