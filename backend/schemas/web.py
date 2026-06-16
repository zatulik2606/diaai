"""Pydantic DTO for web API (frontend-contract v1)."""

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

Trend = Literal["up", "down", "flat"]
KpiId = Literal["active_patients", "total_xe", "questions_count", "food_events_count"]
SubmissionType = Literal["food_event", "photo_analysis"]
MessageRole = Literal["user", "assistant"]
Medal = Literal["gold", "silver", "bronze"]
BjeMedal = Literal["gold", "silver", "bronze", "fourth", "fifth"]
MatrixPeriod = Literal["week", "month"]
LeaderboardPeriod = Literal["7d", "30d", "90d"]
MetricKey = Literal["xe", "bje", "insulin_dose", "activity_score"]
PatientKpiId = Literal["total_xe", "questions_count", "food_events_count", "insulin_total"]
PatientMetricId = Literal["xe", "bje", "insulin"]


# --- Auth ---


class AuthResolveRequest(BaseModel):
    username: str = Field(min_length=1)


class AuthResolveResponse(BaseModel):
    user_id: UUID
    telegram_id: int | None
    role: str
    display_name: str | None


# --- Dashboard summary ---


class DashboardKpi(BaseModel):
    id: KpiId
    label: str
    value: float
    delta: float
    delta_pct: float
    trend: Trend


class DashboardSummaryResponse(BaseModel):
    period_days: int
    kpis: list[DashboardKpi]


# --- Dashboard activity ---


class ActivityDayPoint(BaseModel):
    date: date
    requests_count: int
    food_events_count: int


class DashboardActivityResponse(BaseModel):
    days: int
    series: list[ActivityDayPoint]


# --- Dashboard questions ---


class PatientBrief(BaseModel):
    user_id: UUID
    display_name: str | None = None
    telegram_id: int | None = None


class QuestionItem(BaseModel):
    id: UUID
    patient: PatientBrief
    content: str | None
    reply: str
    created_at: datetime


class PaginatedQuestionsResponse(BaseModel):
    items: list[QuestionItem]
    total: int
    limit: int
    offset: int


# --- Dashboard submissions ---


class SubmissionPatient(BaseModel):
    user_id: UUID
    display_name: str | None = None


class SubmissionItem(BaseModel):
    id: UUID
    type: SubmissionType
    patient: SubmissionPatient
    title: str
    xe: float | None = None
    bje: float | None = None
    confidence: float | None = None
    recorded_at: datetime
    detail_url: str


class PaginatedSubmissionsResponse(BaseModel):
    items: list[SubmissionItem]
    total: int
    limit: int
    offset: int


# --- Progress matrix ---


class MatrixColumn(BaseModel):
    id: str
    label: str


class MatrixCellMetrics(BaseModel):
    xe: float
    bje: float
    insulin_dose: float


class MatrixCell(BaseModel):
    column_id: str
    score: int
    completion_pct: float
    snapshot_date: datetime | None = None
    metrics: MatrixCellMetrics


class MatrixRow(BaseModel):
    patient: SubmissionPatient
    cells: list[MatrixCell]


class ProgressMatrixResponse(BaseModel):
    period: MatrixPeriod
    columns: list[MatrixColumn]
    rows: list[MatrixRow]


# --- Leaderboard ---


class LeaderboardProduct(BaseModel):
    name: str
    xe: float
    bje: float
    bje_medal: BjeMedal | None = None


class LeaderboardTableRow(BaseModel):
    rank: int
    patient: SubmissionPatient
    progress_pct: float
    products: list[LeaderboardProduct]


class LeaderboardScatterPoint(BaseModel):
    patient_id: UUID
    display_name: str | None = None
    x: float
    y: float


class LeaderboardResponse(BaseModel):
    period: LeaderboardPeriod
    metric: MetricKey
    table: list[LeaderboardTableRow]
    scatter: list[LeaderboardScatterPoint]


# --- Assistant history ---


class HistoryMessage(BaseModel):
    id: str
    role: MessageRole
    text: str
    created_at: datetime


class PaginatedHistoryResponse(BaseModel):
    items: list[HistoryMessage]
    total: int
    limit: int
    offset: int


# --- Patient dashboard ---


class PatientDashboardKpi(BaseModel):
    id: PatientKpiId
    label: str
    value: float
    delta: float
    delta_pct: float
    trend: Trend


class PatientDashboardSummaryResponse(BaseModel):
    period_days: int
    kpis: list[PatientDashboardKpi]


class PatientQuestionItem(BaseModel):
    id: UUID
    content: str | None
    reply: str
    created_at: datetime


class PaginatedPatientQuestionsResponse(BaseModel):
    items: list[PatientQuestionItem]
    total: int
    limit: int
    offset: int


class PatientSubmissionItem(BaseModel):
    id: UUID
    type: SubmissionType
    title: str
    xe: float | None = None
    bje: float | None = None
    confidence: float | None = None
    recorded_at: datetime
    detail_url: str


class PaginatedPatientSubmissionsResponse(BaseModel):
    items: list[PatientSubmissionItem]
    total: int
    limit: int
    offset: int


class PatientMetricCell(BaseModel):
    column_id: str
    value: float
    completion_pct: float
    snapshot_date: datetime | None = None


class PatientMetricRow(BaseModel):
    metric_id: PatientMetricId
    label: str
    cells: list[PatientMetricCell]


class PatientProgressMatrixResponse(BaseModel):
    period: MatrixPeriod
    columns: list[MatrixColumn]
    rows: list[PatientMetricRow]
