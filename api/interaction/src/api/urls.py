from fastapi import APIRouter
from api.endpoints import files

api_router = APIRouter()
api_router.include_router(files.router)