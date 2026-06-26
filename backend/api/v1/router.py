from fastapi import APIRouter

from backend.api.v1 import analytics, assistant, events, media
from backend.api.v1.web.router import router as web_router

api_router = APIRouter()
api_router.include_router(analytics.router)
api_router.include_router(assistant.router)
api_router.include_router(events.router)
api_router.include_router(media.router)
api_router.include_router(web_router)
