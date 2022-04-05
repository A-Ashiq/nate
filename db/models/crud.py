
from typing import Optional, List

from sqlalchemy.orm import Session

from db.models.page import Page
from db.session import yield_db


def get_page_by_id(page_id: int, db: Optional[Session] = None) -> Page:
    if db is None:
        db = yield_db()

    page = db.query(Page).get(page_id)

    if page is None:
        raise PageNotFoundError

    return page


def get_pages(db: Optional[Session] = None) -> List[Page]:
    if db is None:
        db = yield_db()

    return db.query(Page).all()


class PageNotFoundError(Exception):
    ...