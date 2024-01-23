from fastapi import FastAPI

from app.api.charity_project import router
from app.core.config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)

app.include_router(router)
