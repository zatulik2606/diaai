from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import verify_service_token
from backend.database import get_db
from backend.schemas.events import (
    EventCreated,
    FoodEventCreate,
    FoodEventResponse,
    InsulinEventCreate,
)
from backend.services.events_service import EventsService

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/food", status_code=201, response_model=EventCreated)
async def create_food_event(
    body: FoodEventCreate,
    _: None = Depends(verify_service_token),
    db: AsyncSession = Depends(get_db),
) -> EventCreated:
    service = EventsService(db)
    return await service.create_food(body)


@router.get("/food", response_model=list[FoodEventResponse])
async def list_food_events(
    telegram_id: int = Query(...),
    _from: str | None = Query(default=None, alias="from"),
    _to: str | None = Query(default=None, alias="to"),
    _: None = Depends(verify_service_token),
    db: AsyncSession = Depends(get_db),
) -> list[FoodEventResponse]:
    service = EventsService(db)
    return await service.list_food(telegram_id, _from, _to)


@router.post("/insulin", status_code=201, response_model=EventCreated)
async def create_insulin_event(
    body: InsulinEventCreate,
    _: None = Depends(verify_service_token),
    db: AsyncSession = Depends(get_db),
) -> EventCreated:
    service = EventsService(db)
    return await service.create_insulin(body)
