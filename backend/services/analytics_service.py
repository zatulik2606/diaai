from __future__ import annotations

import re
from datetime import UTC, date, datetime, timedelta, time
from typing import Literal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.food_event import FoodEventRepository
from backend.repositories.insulin_event import InsulinEventRepository
from backend.repositories.progress_snapshot import ProgressSnapshotRepository
from backend.repositories.recommendation import RecommendationRepository
from backend.repositories.user import UserRepository
from backend.schemas.analytics import (
    AnalyticsMetricSums,
    AnalyticsPreviousPeriod,
    AnalyticsProgressResponse,
    AnalyticsRecommendationItem,
    AnalyticsRecommendationsResponse,
    AnalyticsSignal,
    AnalyticsSignalsResponse,
)
from backend.services.web_utils import compute_delta_pct

_PERIOD_DAYS: dict[str, int] = {"day": 1, "week": 7, "month": 30}
_SIGNAL_THRESHOLD_PCT = 5.0
_WARNING_THRESHOLD_PCT = 20.0
_DOSE_PATTERN = re.compile(r"\d+\s*(ед\.?|единиц)", re.IGNORECASE)

_METRIC_LABELS = {"xe": "ХЕ", "bje": "БЖЕ", "insulin": "инсулин"}


def period_date_windows(
    period: Literal["day", "week", "month"],
) -> tuple[date, date, date, date]:
    today = datetime.now(UTC).date()
    days = _PERIOD_DAYS[period]
    current_end = today
    current_start = today - timedelta(days=days - 1)
    previous_end = current_start - timedelta(days=1)
    previous_start = previous_end - timedelta(days=days - 1)
    return current_start, current_end, previous_start, previous_end


def dates_to_datetimes(start: date, end: date) -> tuple[datetime, datetime]:
    from_dt = datetime.combine(start, time.min, tzinfo=UTC)
    to_dt = datetime.combine(end + timedelta(days=1), time.min, tzinfo=UTC)
    return from_dt, to_dt


def progress_trend(delta_pct_xe: float) -> Literal["improving", "stable", "worsening"]:
    if delta_pct_xe > _SIGNAL_THRESHOLD_PCT:
        return "worsening"
    if delta_pct_xe < -_SIGNAL_THRESHOLD_PCT:
        return "improving"
    return "stable"


class AnalyticsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._users = UserRepository(session)
        self._food = FoodEventRepository(session)
        self._insulin = InsulinEventRepository(session)
        self._snapshots = ProgressSnapshotRepository(session)
        self._recommendations = RecommendationRepository(session)

    async def get_progress(
        self,
        telegram_id: int,
        period: Literal["day", "week", "month"],
    ) -> AnalyticsProgressResponse:
        user = await self._users.require_diabetic(telegram_id)
        current_start, current_end, previous_start, previous_end = period_date_windows(period)

        snapshot = await self._snapshots.get_by_user_period(user.id, period, current_start)
        if snapshot is not None:
            current_sums = _sums_from_snapshot(snapshot)
            source: Literal["computed", "snapshot"] = "snapshot"
            trend = snapshot.trend  # type: ignore[assignment]
            comment = snapshot.comment
        else:
            current_sums = await self._compute_sums(user.id, current_start, current_end)
            source = "computed"
            comment = None
            trend = "stable"

        previous_sums = await self._compute_sums(user.id, previous_start, previous_end)
        delta_pct = {
            "xe": compute_delta_pct(current_sums.xe, previous_sums.xe),
            "bje": compute_delta_pct(current_sums.bje, previous_sums.bje),
            "insulin": compute_delta_pct(current_sums.insulin, previous_sums.insulin),
        }
        if source == "computed":
            trend = progress_trend(delta_pct["xe"])

        return AnalyticsProgressResponse(
            telegram_id=telegram_id,
            period=period,
            period_start=current_start,
            period_end=current_end,
            sums=current_sums,
            previous_period=AnalyticsPreviousPeriod(
                period_start=previous_start,
                period_end=previous_end,
                sums=previous_sums,
            ),
            delta_pct=delta_pct,
            trend=trend,
            comment=comment,
            source=source,
        )

    async def get_signals(
        self,
        telegram_id: int,
        period: Literal["week", "month"],
    ) -> AnalyticsSignalsResponse:
        progress = await self.get_progress(telegram_id, period)
        signals: list[AnalyticsSignal] = []
        for metric in ("xe", "bje", "insulin"):
            delta = progress.delta_pct[metric]
            direction, code_suffix = _signal_direction(delta)
            label = _METRIC_LABELS[metric]
            if direction == "flat":
                message = f"Показатель {label} за период без существенных изменений"
            elif direction == "up":
                message = (
                    f"Сумма {label} за период выросла на {abs(delta):.1f}% "
                    f"относительно прошлого периода"
                )
            else:
                message = (
                    f"Сумма {label} за период снизилась на {abs(delta):.1f}% "
                    f"относительно прошлого периода"
                )
            severity: Literal["info", "warning"] = (
                "warning" if abs(delta) >= _WARNING_THRESHOLD_PCT else "info"
            )
            signals.append(
                AnalyticsSignal(
                    code=f"{metric}_{code_suffix}",
                    severity=severity,
                    metric=metric,  # type: ignore[arg-type]
                    direction=direction,
                    message=message,
                    delta_pct=delta,
                )
            )
        return AnalyticsSignalsResponse(
            telegram_id=telegram_id,
            period=period,
            signals=signals,
        )

    async def get_recommendations(
        self,
        telegram_id: int,
        *,
        limit: int,
        offset: int,
    ) -> AnalyticsRecommendationsResponse:
        user = await self._users.require_diabetic(telegram_id)
        limit = min(max(limit, 1), 50)
        offset = max(offset, 0)

        rows, total = await self._recommendations.list_by_user_paged(
            user.id, limit=limit, offset=offset
        )
        items = [
            AnalyticsRecommendationItem(
                id=str(row.id),
                type=row.type,  # type: ignore[arg-type]
                text=row.text,
                created_at=row.created_at,
            )
            for row in rows
            if not _DOSE_PATTERN.search(row.text)
        ]

        if offset == 0 and not items:
            progress = await self.get_progress(telegram_id, "week")
            items = _rule_based_recommendations(progress)
            total = len(items)
            items = items[:limit]

        return AnalyticsRecommendationsResponse(
            telegram_id=telegram_id,
            items=items,
            total=total,
            limit=limit,
            offset=offset,
        )

    async def _compute_sums(
        self,
        user_id: UUID,
        period_start: date,
        period_end: date,
    ) -> AnalyticsMetricSums:
        from_dt, to_dt = dates_to_datetimes(period_start, period_end)
        user_ids = [user_id]
        nutrition = await self._food.sum_nutrition_in_window(user_ids, from_dt, to_dt)
        insulin_map = await self._insulin.sum_dose_by_user(user_ids, from_dt, to_dt)
        insulin = round(float(insulin_map.get(user_id, 0.0)), 1)
        return AnalyticsMetricSums(
            xe=nutrition["xe"] or 0.0,
            bje=nutrition["bje"] or 0.0,
            insulin=insulin,
            proteins=nutrition["proteins"],
            fats=nutrition["fats"],
            carbs=nutrition["carbs"],
        )


def _sums_from_snapshot(snapshot) -> AnalyticsMetricSums:
    return AnalyticsMetricSums(
        xe=float(snapshot.sum_xe),
        bje=float(snapshot.sum_bje),
        insulin=float(snapshot.sum_insulin),
        proteins=float(snapshot.sum_proteins) if snapshot.sum_proteins is not None else None,
        fats=float(snapshot.sum_fats) if snapshot.sum_fats is not None else None,
        carbs=float(snapshot.sum_carbs) if snapshot.sum_carbs is not None else None,
    )


def _signal_direction(delta_pct: float) -> tuple[Literal["up", "down", "flat"], str]:
    if abs(delta_pct) < _SIGNAL_THRESHOLD_PCT:
        return "flat", "stable"
    if delta_pct > 0:
        return "up", "up"
    return "down", "down"


def _rule_based_recommendations(
    progress: AnalyticsProgressResponse,
) -> list[AnalyticsRecommendationItem]:
    now = datetime.now(UTC)
    items: list[AnalyticsRecommendationItem] = []
    xe_delta = progress.delta_pct["xe"]
    if xe_delta > _SIGNAL_THRESHOLD_PCT:
        items.append(
            AnalyticsRecommendationItem(
                id="00000000-0000-4000-8000-000000000101",
                type="nutrition",
                text=(
                    "За период сумма ХЕ выше прошлого окна — "
                    "имеет смысл сверить перекусы с дневником."
                ),
                created_at=now,
            )
        )
    elif abs(xe_delta) <= _SIGNAL_THRESHOLD_PCT:
        items.append(
            AnalyticsRecommendationItem(
                id="00000000-0000-4000-8000-000000000102",
                type="dynamics",
                text="Динамика ХЕ стабильна — продолжайте фиксировать приёмы пищи.",
                created_at=now,
            )
        )
    insulin_delta = progress.delta_pct["insulin"]
    if abs(insulin_delta) <= _SIGNAL_THRESHOLD_PCT:
        items.append(
            AnalyticsRecommendationItem(
                id="00000000-0000-4000-8000-000000000103",
                type="insulin",
                text=(
                    "Общий учтённый инсулин за период без существенных изменений — "
                    "обсудите схему с врачом при необходимости."
                ),
                created_at=now,
            )
        )
    return items
