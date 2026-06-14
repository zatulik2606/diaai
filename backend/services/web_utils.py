"""Shared helpers for web services."""

from datetime import UTC, date, datetime, timedelta

from backend.schemas.web import Medal, Trend


def clamp_limit(limit: int, *, default: int = 20, maximum: int = 100) -> int:
    if limit <= 0:
        return default
    return min(limit, maximum)


def clamp_offset(offset: int) -> int:
    return max(0, offset)


def compute_trend(delta: float) -> Trend:
    if delta > 0:
        return "up"
    if delta < 0:
        return "down"
    return "flat"


def compute_delta_pct(current: float, previous: float) -> float:
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round((current - previous) / previous * 100, 1)


def period_window_days(days: int) -> tuple[datetime, datetime, datetime, datetime]:
    """Return (current_from, current_to, previous_from, previous_to) in UTC."""
    now = datetime.now(UTC)
    current_to = now
    current_from = now - timedelta(days=days)
    previous_to = current_from
    previous_from = current_from - timedelta(days=days)
    return current_from, current_to, previous_from, previous_to


def leaderboard_days(period: str) -> int:
    mapping = {"7d": 7, "30d": 30, "90d": 90}
    return mapping.get(period, 30)


def activity_start_day(days: int) -> date:
    today = datetime.now(UTC).date()
    return today - timedelta(days=days - 1)


def week_column(period_start: date) -> tuple[str, str]:
    iso = period_start.isocalendar()
    column_id = f"{iso.year}-W{iso.week:02d}"
    label = f"W{iso.week}"
    return column_id, label


def snapshot_score(sum_xe: float) -> int:
    return min(100, int(sum_xe / 60 * 100))


def medal_for_rank(rank: int) -> Medal | None:
    if rank == 1:
        return "gold"
    if rank == 2:
        return "silver"
    if rank == 3:
        return "bronze"
    return None
