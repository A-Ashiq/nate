"""
This module holds the main FastAPI application instance
"""
from fastapi import FastAPI

from db.session import Base, engine
from routers import health, pages

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(pages.router)
