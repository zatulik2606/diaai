from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import func, select, union
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.food_event import FoodEvent
from backend.models.progress_snapshot import ProgressSnapshot
from backend.models.request import DialogRequest
from backend.repositories.food_event import FoodEventRepository
from backend.repositories.progress_snapshot import ProgressSnapshotRepository
from backend.repositories.request import RequestRepository
from backend.repositories.user import UserRepository
from backend.repositories.web_submission import WebSubmissionRepository
from backend.schemas.web import (
    ActivityDayPoint,
    DashboardActivityResponse,
    DashboardKpi,
    DashboardSummaryResponse,
    KpiId,
    MatrixCell,
    MatrixCellMetrics,
    MatrixColumn,
    MatrixPeriod,
    MatrixRow,
    PaginatedQuestionsResponse,
    PaginatedSubmissionsResponse,
    PatientBrief,
    ProgressMatrixResponse,
    QuestionItem,
    SubmissionItem,
    SubmissionPatient,
)
from backend.services.web_utils import (
    activity_start_day,
    compute_delta_pct,
    compute_trend,
    period_window_days,
    snapshot_score,
    week_column,
)

KPI_LABELS: dict[KpiId, str] = {
    "active_patients": "Активные пациенты",
    "total_xe": "Сумма ХЕ",
    "questions_count": "Вопросов",
    "food_events_count": "Событий питания",
}


class WebDoctorService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._users = UserRepository(session)
        self._food = FoodEventRepository(session)
        self._requests = RequestRepository(session)
        self._submissions = WebSubmissionRepository(session)
        self._snapshots = ProgressSnapshotRepository(session)

    async def _cohort_ids(self) -> list[UUID]:
        patients = await self._users.list_diabetics()
        return [patient.id for patient in patients]

    async def _count_active_patients(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> int:
        if not user_ids:
            return 0
        food_users = select(FoodEvent.user_id).where(
            FoodEvent.user_id.in_(user_ids),
            FoodEvent.recorded_at >= from_dt,
            FoodEvent.recorded_at < to_dt,
        )
        request_users = select(DialogRequest.user_id).where(
            DialogRequest.user_id.in_(user_ids),
            DialogRequest.created_at >= from_dt,
            DialogRequest.created_at < to_dt,
        )
        combined = union(food_users, request_users).subquery()
        result = await self._session.scalar(select(func.count()).select_from(combined))
        return int(result or 0)

    async def get_summary(self, *, period_days: int) -> DashboardSummaryResponse:
        user_ids = await self._cohort_ids()
        current_from, current_to, prev_from, prev_to = period_window_days(period_days)

        metrics = {
            "active_patients": (
                await self._count_active_patients(user_ids, current_from, current_to),
                await self._count_active_patients(user_ids, prev_from, prev_to),
            ),
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
        }

        kpis: list[DashboardKpi] = []
        for kpi_id, label in KPI_LABELS.items():
            current, previous = metrics[kpi_id]
            delta = current - previous
            kpis.append(
                DashboardKpi(
                    id=kpi_id,
                    label=label,
                    value=round(current, 1),
                    delta=round(delta, 1),
                    delta_pct=compute_delta_pct(current, previous),
                    trend=compute_trend(delta),
                )
            )

        return DashboardSummaryResponse(period_days=period_days, kpis=kpis)

    async def get_activity(self, *, days: int) -> DashboardActivityResponse:
        user_ids = await self._cohort_ids()
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
        *,
        limit: int,
        offset: int,
    ) -> PaginatedQuestionsResponse:
        user_ids = await self._cohort_ids()
        rows, total = await self._requests.list_questions_for_users(
            user_ids, limit=limit, offset=offset
        )
        items = [
            QuestionItem(
                id=req.id,
                patient=PatientBrief(
                    user_id=user.id,
                    display_name=user.display_name,
                    telegram_id=user.telegram_id,
                ),
                content=req.content,
                reply=req.reply,
                created_at=req.created_at,
            )
            for req, user in rows
        ]
        return PaginatedQuestionsResponse(items=items, total=total, limit=limit, offset=offset)

    async def get_submissions(
        self,
        *,
        limit: int,
        offset: int,
    ) -> PaginatedSubmissionsResponse:
        user_ids = await self._cohort_ids()
        rows, total = await self._submissions.list_for_users(user_ids, limit=limit, offset=offset)
        items = [
            SubmissionItem(
                id=row.id,
                type=row.submission_type,
                patient=SubmissionPatient(
                    user_id=row.user_id,
                    display_name=row.display_name,
                ),
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
        return PaginatedSubmissionsResponse(items=items, total=total, limit=limit, offset=offset)

    async def get_progress_matrix(self, *, period: MatrixPeriod) -> ProgressMatrixResponse:
        user_ids = await self._cohort_ids()
        patients = await self._users.list_diabetics()
        snapshots = await self._snapshots.list_for_users(user_ids, period=period)

        columns_map: dict[str, MatrixColumn] = {}
        snapshot_index: dict[tuple[UUID, str], ProgressSnapshot] = {}
        for snap in snapshots:
            column_id, label = week_column(snap.period_start)
            columns_map[column_id] = MatrixColumn(id=column_id, label=label)
            snapshot_index[(snap.user_id, column_id)] = snap

        columns = sorted(columns_map.values(), key=lambda col: col.id)
        rows: list[MatrixRow] = []
        for patient in patients:
            cells: list[MatrixCell] = []
            for column in columns:
                snap = snapshot_index.get((patient.id, column.id))
                if snap is None:
                    cells.append(
                        MatrixCell(
                            column_id=column.id,
                            score=0,
                            completion_pct=0.0,
                            metrics=MatrixCellMetrics(xe=0.0, bje=0.0, insulin_dose=0.0),
                        )
                    )
                    continue
                score = snapshot_score(float(snap.sum_xe))
                cells.append(
                    MatrixCell(
                        column_id=column.id,
                        score=score,
                        completion_pct=float(score),
                        snapshot_date=datetime.combine(
                            snap.period_end, datetime.min.time(), tzinfo=UTC
                        ),
                        metrics=MatrixCellMetrics(
                            xe=float(snap.sum_xe),
                            bje=float(snap.sum_bje),
                            insulin_dose=float(snap.sum_insulin),
                        ),
                    )
                )
            rows.append(
                MatrixRow(
                    patient=SubmissionPatient(
                        user_id=patient.id,
                        display_name=patient.display_name,
                    ),
                    cells=cells,
                )
            )

        return ProgressMatrixResponse(
            period=period,
            columns=columns,
            rows=rows,
        )
