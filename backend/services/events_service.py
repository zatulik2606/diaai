from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.exceptions import AppError
from backend.repositories.food_event import FoodEventRepository
from backend.repositories.insulin_event import InsulinEventRepository
from backend.repositories.request import RequestRepository
from backend.repositories.user import UserRepository
from backend.schemas.events import (
    EventCreated,
    FoodEventCreate,
    FoodEventResponse,
    FoodSource,
    InsulinEventCreate,
)


class EventsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._users = UserRepository(session)
        self._requests = RequestRepository(session)
        self._food = FoodEventRepository(session)
        self._insulin = InsulinEventRepository(session)

    async def create_food(self, body: FoodEventCreate) -> EventCreated:
        user = await self._users.get_or_create(body.telegram_id)
        request_id = _parse_optional_uuid(body.request_id)
        if request_id is not None:
            await _ensure_request_owned(self._requests, request_id, user.id)

        event = await self._food.create(
            user_id=user.id,
            description=body.description,
            xe=body.xe,
            bje=body.bje,
            source=body.source,
            proteins=body.proteins,
            fats=body.fats,
            carbs=body.carbs,
            request_id=request_id,
            comment=body.comment,
        )
        return _event_created(event.id, event.recorded_at)

    async def create_insulin(self, body: InsulinEventCreate) -> EventCreated:
        user = await self._users.get_or_create(body.telegram_id)
        food_event_id = _parse_optional_uuid(body.food_event_id)
        if food_event_id is not None:
            food = await self._food.get_by_id(food_event_id)
            if food is None:
                raise AppError(
                    code="NOT_FOUND",
                    message="Food event not found",
                    status_code=404,
                )
            if food.user_id != user.id:
                raise AppError(
                    code="FORBIDDEN",
                    message="Food event belongs to another user",
                    status_code=403,
                )

        injected_at = _parse_injected_at(body.injected_at)
        event = await self._insulin.create(
            user_id=user.id,
            dose=body.dose,
            injected_at=injected_at,
            food_event_id=food_event_id,
            comment=body.comment,
        )
        return _event_created(event.id, event.recorded_at)

    async def list_food(
        self,
        telegram_id: int,
        from_raw: str | None,
        to_raw: str | None,
    ) -> list[FoodEventResponse]:
        user = await self._users.get_or_create(telegram_id)
        from_dt = _parse_datetime_query(from_raw, "from")
        to_dt = _parse_datetime_query(to_raw, "to")
        events = await self._food.list_for_user(user.id, from_dt, to_dt)
        return [_food_to_response(e, telegram_id) for e in events]


async def _ensure_request_owned(
    requests: RequestRepository, request_id: uuid.UUID, user_id: uuid.UUID
) -> None:
    record = await requests.get_by_id(request_id)
    if record is None:
        raise AppError(
            code="NOT_FOUND",
            message="Request not found",
            status_code=404,
        )
    if record.user_id != user_id:
        raise AppError(
            code="FORBIDDEN",
            message="Request belongs to another user",
            status_code=403,
        )


def _parse_optional_uuid(value: str | None) -> uuid.UUID | None:
    if value is None:
        return None
    try:
        return uuid.UUID(value)
    except ValueError as exc:
        raise AppError(
            code="BAD_REQUEST",
            message="Invalid UUID format",
            status_code=422,
        ) from exc


def _parse_injected_at(value: str | None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AppError(
            code="BAD_REQUEST",
            message="Invalid injected_at format",
            status_code=422,
        ) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed


def _parse_datetime_query(value: str | None, field: str) -> datetime | None:
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AppError(
            code="BAD_REQUEST",
            message=f"Invalid {field} datetime format",
            status_code=422,
        ) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed


def _event_created(event_id: uuid.UUID, recorded_at: datetime) -> EventCreated:
    return EventCreated(
        id=str(event_id),
        recorded_at=_format_dt(recorded_at),
    )


def _format_dt(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _food_to_response(event, telegram_id: int) -> FoodEventResponse:
    return FoodEventResponse(
        id=str(event.id),
        telegram_id=telegram_id,
        description=event.description,
        xe=float(event.xe),
        bje=float(event.bje),
        proteins=float(event.proteins) if event.proteins is not None else None,
        fats=float(event.fats) if event.fats is not None else None,
        carbs=float(event.carbs) if event.carbs is not None else None,
        source=FoodSource(event.source),
        request_id=str(event.request_id) if event.request_id else None,
        comment=event.comment,
        recorded_at=_format_dt(event.recorded_at),
    )
