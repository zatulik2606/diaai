from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.progress_snapshot import ProgressSnapshot
from backend.models.user import User
from backend.repositories.food_event import FoodEventRepository
from backend.repositories.insulin_event import InsulinEventRepository
from backend.repositories.progress_snapshot import ProgressSnapshotRepository
from backend.repositories.request import RequestRepository
from backend.repositories.web_submission import WebSubmissionRepository
from backend.schemas.web import (
    ActivityDayPoint,
    DashboardActivityResponse,
    MatrixColumn,
    MatrixPeriod,
    PaginatedPatientQuestionsResponse,
    PaginatedPatientSubmissionsResponse,
    PatientDashboardKpi,
    PatientDashboardSummaryResponse,
    PatientKpiId,
    PatientMetricCell,
    PatientMetricId,
    PatientMetricRow,
    PatientProgressMatrixResponse,
    PatientQuestionItem,
    PatientSubmissionItem,
)
from backend.services.web_utils import (
    activity_start_day,
    compute_delta_pct,
    compute_trend,
    period_window_days,
    snapshot_score,
    week_column,
)

PATIENT_KPI_LABELS: dict[PatientKpiId, str] = {
    "total_xe": "Сумма ХЕ",
    "questions_count": "Вопросов",
    "food_events_count": "Событий питания",
    "insulin_total": "Инсулин",
}

METRIC_LABELS: dict[PatientMetricId, str] = {
    "xe": "ХЕ",
    "bje": "БЖЕ",
    "insulin": "Инсулин",
}


class WebPatientService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._food = FoodEventRepository(session)
        self._requests = RequestRepository(session)
        self._submissions = WebSubmissionRepository(session)
        self._snapshots = ProgressSnapshotRepository(session)
        self._insulin = InsulinEventRepository(session)

    async def get_summary(
        self,
        patient: User,
        *,
        period_days: int,
    ) -> PatientDashboardSummaryResponse:
        user_ids = [patient.id]
        current_from, current_to, prev_from, prev_to = period_window_days(period_days)

        insulin_current = await self._insulin.sum_dose_by_user(user_ids, current_from, current_to)
        insulin_prev = await self._insulin.sum_dose_by_user(user_ids, prev_from, prev_to)

        metrics = {
            "total_xe": (
                await self._food.sum_xe_in_window(user_ids, current_from, current_to),
                await self._food.sum_xe_in_window(user_ids, prev_from, prev_to),
            ),
            "questions_count": (
                float(await self._requests.count_in_window(user_ids, current_from, current_to)),
                float(await self._requests.count_in_window(user_ids, prev_from, prev_to)),
            ),
            "food_events_count": (
                float(await self._food.count_in_window(user_ids, current_from, current_to)),
                float(await self._food.count_in_window(user_ids, prev_from, prev_to)),
            ),
            "insulin_total": (
                float(insulin_current.get(patient.id, 0.0)),
                float(insulin_prev.get(patient.id, 0.0)),
            ),
        }

        kpis: list[PatientDashboardKpi] = []
        for kpi_id, label in PATIENT_KPI_LABELS.items():
            current, previous = metrics[kpi_id]
            delta = current - previous
            kpis.append(
                PatientDashboardKpi(
                    id=kpi_id,
                    label=label,
                    value=round(current, 1),
                    delta=round(delta, 1),
                    delta_pct=compute_delta_pct(current, previous),
                    trend=compute_trend(delta),
                )
            )

        return PatientDashboardSummaryResponse(period_days=period_days, kpis=kpis)

    async def get_activity(self, patient: User, *, days: int) -> DashboardActivityResponse:
        user_ids = [patient.id]
        from_day = activity_start_day(days)
        food_by_day = await self._food.daily_counts(user_ids, from_day, days)
        requests_by_day = await self._requests.daily_counts(user_ids, from_day, days)

        series: list[ActivityDayPoint] = []
        for offset in range(days):
            day = from_day + timedelta(days=offset)
            series.append(
                ActivityDayPoint(
                    date=day,
                    requests_count=requests_by_day.get(day, 0),
                    food_events_count=food_by_day.get(day, 0),
                )
            )
        return DashboardActivityResponse(days=days, series=series)

    async def get_questions(
        self,
        patient: User,
        *,
        limit: int,
        offset: int,
    ) -> PaginatedPatientQuestionsResponse:
        rows, total = await self._requests.list_questions_for_users(
            [patient.id], limit=limit, offset=offset
        )
        items = [
            PatientQuestionItem(
                id=req.id,
                content=req.content,
                reply=req.reply,
                created_at=req.created_at,
            )
            for req, _user in rows
        ]
        return PaginatedPatientQuestionsResponse(
            items=items, total=total, limit=limit, offset=offset
        )

    async def get_submissions(
        self,
        patient: User,
        *,
        limit: int,
        offset: int,
    ) -> PaginatedPatientSubmissionsResponse:
        rows, total = await self._submissions.list_for_users(
            [patient.id], limit=limit, offset=offset
        )
        items = [
            PatientSubmissionItem(
                id=row.id,
                type=row.submission_type,
                title=row.title,
                xe=row.xe,
                bje=row.bje,
                confidence=row.confidence,
                recorded_at=row.recorded_at,
                detail_url=(
                    f"/patients/{row.user_id}/events/{row.id}"
                    if row.submission_type == "food_event"
                    else f"/patients/{row.user_id}/photos/{row.id}"
                ),
            )
            for row in rows
        ]
        return PaginatedPatientSubmissionsResponse(
            items=items, total=total, limit=limit, offset=offset
        )

    async def get_progress_matrix(
        self,
        patient: User,
        *,
        period: MatrixPeriod,
    ) -> PatientProgressMatrixResponse:
        snapshots = await self._snapshots.list_for_users([patient.id], period=period)

        columns_map: dict[str, MatrixColumn] = {}
        snapshot_index: dict[str, ProgressSnapshot] = {}
        for snap in snapshots:
            column_id, label = week_column(snap.period_start)
            columns_map[column_id] = MatrixColumn(id=column_id, label=label)
            snapshot_index[column_id] = snap

        columns = sorted(columns_map.values(), key=lambda col: col.id)

        def cell_for_metric(
            metric_id: PatientMetricId,
            snap: ProgressSnapshot | None,
            column_id: str,
        ) -> PatientMetricCell:
            if snap is None:
                return PatientMetricCell(
                    column_id=column_id,
                    value=0.0,
                    completion_pct=0.0,
                )
            if metric_id == "xe":
                value = float(snap.sum_xe)
                pct = float(snapshot_score(value))
            elif metric_id == "bje":
                value = float(snap.sum_bje)
                pct = float(snapshot_score(value))
            else:
                value = float(snap.sum_insulin)
                pct = float(snapshot_score(value))
            return PatientMetricCell(
                column_id=column_id,
                value=round(value, 1),
                completion_pct=pct,
                snapshot_date=datetime.combine(snap.period_end, datetime.min.time(), tzinfo=UTC),
            )

        rows: list[PatientMetricRow] = []
        for metric_id, label in METRIC_LABELS.items():
            cells = [
                cell_for_metric(metric_id, snapshot_index.get(column.id), column.id)
                for column in columns
            ]
            rows.append(PatientMetricRow(metric_id=metric_id, label=label, cells=cells))

        return PatientProgressMatrixResponse(
            period=period,
            columns=columns,
            rows=rows,
        )
