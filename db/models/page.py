from typing import Dict, Optional

from sqlalchemy import Column, DateTime, Integer, String, JSON
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from db.session import Base, yield_db


class Page(Base):
    __tablename__ = "page"
    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String)
    status = Column(String)
    results = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @classmethod
    def create(cls, db: Optional[Session] = None, **kwargs):
        page = cls(**kwargs)
        db.add(page)
        db.commit()
        return page

    def _update_status(self, status: str, db: Optional[Session] = None) -> None:
        if db is None:
            db = yield_db()

        self.status = status
        db.add(self)
        db.commit()

    def update_status_to_started(self, db: Optional[Session] = None) -> None:
        return self._update_status(status="STARTED", db=db)

    def update_status_to_done(self, db: Optional[Session] = None) -> None:
        return self._update_status(status="DONE", db=db)

    def update_status_to_failed(self, db: Optional[Session] = None) -> None:
        return self._update_status(status="FAILED", db=db)

    def get_results_ordered_by_frequency(self) -> Dict[str, int]:
        try:
            return dict(
                sorted(self.results.items(), key=lambda item: item[1], reverse=True)
            )
        except AttributeError:
            return {}

    def get_results_ordered_by_alphabetical(self) -> Dict[str, int]:
        try:
            return dict(sorted(self.results.items(), key=lambda item: item[0]))
        except AttributeError:
            return {}
