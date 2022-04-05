"""
This module holds schema models for the `page` router
"""
from pydantic import BaseModel


class PagePostSchema(BaseModel):
    """
    Schema model to receive on page creation.
    """
    target_url: str
