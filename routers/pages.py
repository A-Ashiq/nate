"""
This module holds the API layer/endpoints for the `pages` router
"""
from typing import Optional

import schemas
import serializers
from async_execution.tasks import run_scrape_page_task
from db.models import crud
from db.models.page import Page
from db.session import yield_db
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/pages/", tags=["pages"])
async def create_page(page: schemas.PagePostSchema, db: Session = Depends(yield_db)):
    """
    Create a `Page` object and kick off an asynchronous task to scrape text from the page.

    This endpoint will return the ID of the newly created `Page` object.

    The `GET /pages/{page_id}` endpoint must then be polled with the ID to see the results.
    """
    page_model = Page.create(target_url=page.target_url, db=db)

    run_scrape_page_task.si(page_id=page_model.id).apply_async()

    return {"page_id": page_model.id}


@router.get(
    "/pages/",
    tags=["pages"],
)
async def read_pages(db: Session = Depends(yield_db)):
    """
    List information about the `Page` objects.

    This includes the status of the page also include the results themselves.

    To be able to order results for a particular page,
    hit the `GET /pages/{page_id}/` endpoint with the corresponding `page_id`.
    """
    return crud.get_pages(db=db)


ordering_examples = {
    "unordered": {
        "description": "No ordering will be applied to the results.",
        "value": "unordered",
    },
    "frequency": {
        "description": "Sorts text results by frequency of occurrence in descending order. "
        "Starting from the most frequent.",
        "value": "frequency",
    },
    "alphabetical": {
        "description": "Sorts text results by alphabetical order in descending order. "
        "Starting from `'A'`.",
        "value": "alphabetical",
    },
}


@router.get("/pages/{page_id}", tags=["pages"])
async def read_page(
    page_id: int,
    ordering: Optional[str] = Query(
        "unordered",
        examples=ordering_examples,
        description="The ordering of which to display the results",
    ),
    db: Session = Depends(yield_db),
):
    """
    Retrieve the results from a page.

    This includes the status of the page as well as the results themselves.

    To order results pass one of the following strings to the `ordering` field:

    - `alphabetical`: Returns results ranked by alphabetical order, in descending order only.

    - `frequency`: Returns results ranked by frequency, in descending order only.
    """
    try:
        page_model = crud.get_page_by_id(page_id=page_id, db=db)
    except crud.PageNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")

    page_serializer = serializers.PageSerializer(page=page_model, ordering=ordering)
    return page_serializer.retrieve_output()
