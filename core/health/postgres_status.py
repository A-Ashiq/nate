"""
This module holds functionality for checking the status of Postgres
"""
from typing import Optional

from sqlalchemy.orm import Session

from db.session import yield_db


def postgres_is_healthy(db: Optional[Session] = None) -> bool:
    """
    Checks if the database can be reached by executing a query.

    Returns:
        True if the database is available, False otherwise.

    """
    if db is None:
        db = next(yield_db())

    try:
        return bool(db.execute('SELECT 1'))
    except ValueError:
        return False
