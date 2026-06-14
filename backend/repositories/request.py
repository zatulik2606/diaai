import uuid
from datetime import date, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Date, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.request import DialogRequest
from backend.models.user import User


class RequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, request_id: uuid.UUID) -> DialogRequest | None:
        return await self._session.get(DialogRequest, request_id)

    async def list_for_dialog(self, dialog_id: uuid.UUID, limit: int) -> list[DialogRequest]:
        result = await self._session.execute(
            select(DialogRequest)
            .where(DialogRequest.dialog_id == dialog_id)
            .order_by(DialogRequest.created_at.desc())
            .limit(limit)
        )
        rows = list(result.scalars().all())
        rows.reverse()
        return rows

    async def create(
        self,
        *,
        dialog_id: uuid.UUID,
        user_id: uuid.UUID,
        request_type: str,
        content: str | None,
        reply: str,
        media: dict[str, Any] | None = None,
    ) -> DialogRequest:
        record = DialogRequest(
            dialog_id=dialog_id,
            user_id=user_id,
            type=request_type,
            content=content,
            reply=reply,
            media=media,
        )
        self._session.add(record)
        await self._session.flush()
        return record

    async def count_in_window(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
        *,
        types: tuple[str, ...] = ("text", "mixed"),
    ) -> int:
        if not user_ids:
            return 0
        result = await self._session.scalar(
            select(func.count())
            .select_from(DialogRequest)
            .where(
                DialogRequest.user_id.in_(user_ids),
                DialogRequest.type.in_(types),
                DialogRequest.created_at >= from_dt,
                DialogRequest.created_at < to_dt,
            )
        )
        return int(result or 0)

    async def count_distinct_users_in_window(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> int:
        if not user_ids:
            return 0
        result = await self._session.scalar(
            select(func.count(func.distinct(DialogRequest.user_id))).where(
                DialogRequest.user_id.in_(user_ids),
                DialogRequest.created_at >= from_dt,
                DialogRequest.created_at < to_dt,
            )
        )
        return int(result or 0)

    async def daily_counts(
        self,
        user_ids: list[UUID],
        from_day: date,
        days: int,
    ) -> dict[date, int]:
        if not user_ids or days <= 0:
            return {}
        to_day = from_day.toordinal() + days
        to_date = date.fromordinal(to_day)
        day_col = cast(DialogRequest.created_at, Date)
        result = await self._session.execute(
            select(day_col, func.count())
            .where(
                DialogRequest.user_id.in_(user_ids),
                day_col >= from_day,
                day_col < to_date,
            )
            .group_by(day_col)
        )
        return {row[0]: int(row[1]) for row in result.all()}

    async def list_questions_for_users(
        self,
        user_ids: list[UUID],
        *,
        limit: int,
        offset: int,
    ) -> tuple[list[tuple[DialogRequest, User]], int]:
        if not user_ids:
            return [], 0
        base = (
            select(DialogRequest, User)
            .join(User, DialogRequest.user_id == User.id)
            .where(
                DialogRequest.user_id.in_(user_ids),
                DialogRequest.type.in_(("text", "mixed")),
            )
        )
        total = await self._session.scalar(
            select(func.count())
            .select_from(DialogRequest)
            .where(
                DialogRequest.user_id.in_(user_ids),
                DialogRequest.type.in_(("text", "mixed")),
            )
        )
        result = await self._session.execute(
            base.order_by(DialogRequest.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.all()), int(total or 0)

    async def count_by_user(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> dict[UUID, int]:
        if not user_ids:
            return {}
        result = await self._session.execute(
            select(DialogRequest.user_id, func.count())
            .where(
                DialogRequest.user_id.in_(user_ids),
                DialogRequest.created_at >= from_dt,
                DialogRequest.created_at < to_dt,
            )
            .group_by(DialogRequest.user_id)
        )
        return {row[0]: int(row[1]) for row in result.all()}

    async def count_for_user(self, user_id: UUID) -> int:
        result = await self._session.scalar(
            select(func.count()).select_from(DialogRequest).where(DialogRequest.user_id == user_id)
        )
        return int(result or 0)

    async def list_for_user_history(
        self,
        user_id: UUID,
        *,
        limit: int,
        offset: int,
    ) -> tuple[list[DialogRequest], int]:
        total = await self._session.scalar(
            select(func.count()).select_from(DialogRequest).where(DialogRequest.user_id == user_id)
        )
        result = await self._session.execute(
            select(DialogRequest)
            .where(DialogRequest.user_id == user_id)
            .order_by(DialogRequest.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all()), int(total or 0)
