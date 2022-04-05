"""
This module holds the API layer/endpoints for the `health` router
"""
from fastapi import APIRouter
from core.health.status import get_health_statuses

router = APIRouter()


@router.get("/health/", tags=["health"])
async def get_health():
    """
    Gets the health statuses of services throughout the application.

    Currently a service can be considered in 2 possible states:

    - `"HEALTHY"`: If the service responded to the probe.

    - `"UNHEALTHY"`: If the service did not respond to the probe.
    """
    return get_health_statuses()
