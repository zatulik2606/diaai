from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

AnalyticsPeriod = Literal["day", "week", "month"]
SignalsPeriod = Literal["week", "month"]
ProgressTrend = Literal["improving", "stable", "worsening"]
ProgressSource = Literal["computed", "snapshot"]
SignalSeverity = Literal["info", "warning"]
SignalMetric = Literal["xe", "bje", "insulin"]
SignalDirection = Literal["up", "down", "flat"]
RecommendationType = Literal["nutrition", "insulin", "dynamics"]


class AnalyticsMetricSums(BaseModel):
    xe: float
    bje: float
    insulin: float
    proteins: float | None = None
    fats: float | None = None
    carbs: float | None = None


class AnalyticsPreviousPeriod(BaseModel):
    period_start: date
    period_end: date
    sums: AnalyticsMetricSums


class AnalyticsProgressResponse(BaseModel):
    telegram_id: int
    period: AnalyticsPeriod
    period_start: date
    period_end: date
    sums: AnalyticsMetricSums
    previous_period: AnalyticsPreviousPeriod
    delta_pct: dict[str, float] = Field(..., description="xe, bje, insulin percentages")
    trend: ProgressTrend
    comment: str | None = None
    source: ProgressSource


class AnalyticsSignal(BaseModel):
    code: str
    severity: SignalSeverity
    metric: SignalMetric
    direction: SignalDirection
    message: str
    delta_pct: float


class AnalyticsSignalsResponse(BaseModel):
    telegram_id: int
    period: SignalsPeriod
    signals: list[AnalyticsSignal]


class AnalyticsRecommendationItem(BaseModel):
    id: str
    type: RecommendationType
    text: str
    created_at: datetime


class AnalyticsRecommendationsResponse(BaseModel):
    telegram_id: int
    items: list[AnalyticsRecommendationItem]
    total: int
    limit: int
    offset: int
