"""
This module holds decorated asynchronous tasks
"""
from application.pages.scrape import run_scrape_page
from celery_app import celery
from db.models import crud
from db.session import SessionLocal


@celery.task(ignore_result=True)
def run_scrape_page_task(page_id: int):
    """
    Calls `run_scrape_page()` within the context of a celery task.

    Args:
        page_id: The ID of the `Page` object to be scraped.

    Returns:
        None

    """
    db = SessionLocal()
    page = crud.get_page_by_id(page_id=page_id, db=db)
    run_scrape_page(page=page, db=db)
