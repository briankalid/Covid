from fastapi import FastAPI

from core.settings import settings
from api.urls import api_router

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1}/openapi.json", docs_url="/docs")

app.include_router(api_router, prefix=settings.API_V1)
