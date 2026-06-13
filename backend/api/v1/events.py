from fastapi import APIRouter, Depends, Query

from backend.api.deps import verify_service_token
from backend.exceptions import AppError
from backend.schemas.events import FoodEventCreate, InsulinEventCreate

router = APIRouter(prefix="/events", tags=["events"])


def _not_implemented() -> None:
    raise AppError(
        code="NOT_IMPLEMENTED",
        message="Endpoint not implemented yet",
        status_code=501,
    )


@router.post("/food", status_code=201)
async def create_food_event(
    body: FoodEventCreate,
    _: None = Depends(verify_service_token),
) -> None:
    _not_implemented()


@router.get("/food")
async def list_food_events(
    telegram_id: int = Query(...),
    _from: str | None = Query(default=None, alias="from"),
    _to: str | None = Query(default=None, alias="to"),
    _: None = Depends(verify_service_token),
) -> None:
    _not_implemented()


@router.post("/insulin", status_code=201)
async def create_insulin_event(
    body: InsulinEventCreate,
    _: None = Depends(verify_service_token),
) -> None:
    _not_implemented()
