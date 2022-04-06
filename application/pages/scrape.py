"""
This module holds functionality for scraping a page.
"""
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from core.pages.statistics import get_page_text_statistics
from db.models.page import Page


def run_scrape_page(page: Page, db: Optional[Session] = None) -> None:
    """
    Updates the status of the `Page` object
    around the calling of `scrape_page()`.

    Note that `scrape_page()` is responsible for the real computation.
    This function should be considered
    as the synchronous version of the `run_scrape_page_task`.

    Args:
        page: A `Page` object which is to have scraping performed.

    Returns:
        None

    """
    page.update_status_to_started(db=db)

    try:
        scrape_page(page=page)
    except Exception:
        # Logging should be made here so we can see why the action failed
        page.update_status_to_failed(db=db)
        raise

    page.update_status_to_done(db=db)


def scrape_page(page: Page) -> None:
    """
    Scrapes the page by fetching text elements from the `target_url`.
    The results of which are stored as JSON
    on the `results` field of the `Page` object.

    Args:
        page: A `Page` object which is to have scraping performed.

    Returns:
        None

    """
    page_statistics = get_page_text_statistics(page.target_url)

    page.key = str(uuid.uuid4())
    page.results = page_statistics
