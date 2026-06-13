from fastapi import APIRouter

from backend.api.v1 import assistant, events

api_router = APIRouter()
api_router.include_router(assistant.router)
api_router.include_router(events.router)
