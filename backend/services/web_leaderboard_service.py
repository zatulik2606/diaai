from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User
from backend.repositories.food_event import FoodEventRepository
from backend.repositories.insulin_event import InsulinEventRepository
from backend.repositories.progress_snapshot import ProgressSnapshotRepository
from backend.repositories.request import RequestRepository
from backend.repositories.user import UserRepository
from backend.schemas.web import (
    LeaderboardMetrics,
    LeaderboardPeriod,
    LeaderboardResponse,
    LeaderboardScatterPoint,
    LeaderboardTableRow,
    MetricKey,
    SubmissionPatient,
)
from backend.services.web_utils import (
    leaderboard_days,
    medal_for_rank,
    period_window_days,
    snapshot_score,
)


class WebLeaderboardService:
    def __init__(self, session: AsyncSession) -> None:
        self._users = UserRepository(session)
        self._food = FoodEventRepository(session)
        self._insulin = InsulinEventRepository(session)
        self._requests = RequestRepository(session)
        self._snapshots = ProgressSnapshotRepository(session)

    def _metric_value(
        self,
        metric: MetricKey,
        *,
        food: dict[str, float],
        insulin: float,
        requests: int,
    ) -> float:
        if metric == "xe":
            return food.get("xe", 0.0)
        if metric == "bje":
            return food.get("bje", 0.0)
        if metric == "insulin_dose":
            return insulin
        if metric == "activity_score":
            return food.get("food_count", 0.0) + float(requests)
        return 0.0

    async def get_leaderboard(
        self,
        *,
        period: LeaderboardPeriod,
        metric: MetricKey,
        metric_x: MetricKey,
        metric_y: MetricKey,
    ) -> LeaderboardResponse:
        patients = await self._users.list_diabetics()
        user_ids = [patient.id for patient in patients]
        days = leaderboard_days(period)
        from_dt, to_dt, _, _ = period_window_days(days)

        food_by_user = await self._food.aggregate_by_user(user_ids, from_dt, to_dt)
        insulin_by_user = await self._insulin.sum_dose_by_user(user_ids, from_dt, to_dt)
        requests_by_user = await self._requests.count_by_user(user_ids, from_dt, to_dt)
        snapshots = await self._snapshots.list_for_users(user_ids, period="week")
        latest_snapshot: dict[UUID, float] = {}
        for snap in snapshots:
            latest_snapshot[snap.user_id] = float(snap.sum_xe)

        rows_data: list[tuple[User, float, LeaderboardMetrics, float]] = []
        for patient in patients:
            food = food_by_user.get(patient.id, {"xe": 0.0, "bje": 0.0, "food_count": 0.0})
            insulin = insulin_by_user.get(patient.id, 0.0)
            req_count = requests_by_user.get(patient.id, 0)
            metrics = LeaderboardMetrics(
                xe=food.get("xe", 0.0),
                bje=food.get("bje", 0.0),
                insulin_dose=insulin,
            )
            sort_value = self._metric_value(
                metric,
                food=food,
                insulin=insulin,
                requests=req_count,
            )
            progress_pct = float(snapshot_score(latest_snapshot.get(patient.id, 0.0)))
            rows_data.append((patient, sort_value, metrics, progress_pct))

        rows_data.sort(key=lambda row: row[1], reverse=True)

        table: list[LeaderboardTableRow] = []
        scatter: list[LeaderboardScatterPoint] = []
        for rank, (patient, _, metrics, progress_pct) in enumerate(rows_data, start=1):
            food = food_by_user.get(patient.id, {"xe": 0.0, "bje": 0.0, "food_count": 0.0})
            insulin = insulin_by_user.get(patient.id, 0.0)
            req_count = requests_by_user.get(patient.id, 0)
            table.append(
                LeaderboardTableRow(
                    rank=rank,
                    patient=SubmissionPatient(
                        user_id=patient.id,
                        display_name=patient.display_name,
                    ),
                    progress_pct=progress_pct,
                    metrics=metrics,
                    medal=medal_for_rank(rank),
                )
            )
            scatter.append(
                LeaderboardScatterPoint(
                    patient_id=patient.id,
                    display_name=patient.display_name,
                    x=self._metric_value(
                        metric_x,
                        food=food,
                        insulin=insulin,
                        requests=req_count,
                    ),
                    y=self._metric_value(
                        metric_y,
                        food=food,
                        insulin=insulin,
                        requests=req_count,
                    ),
                )
            )

        return LeaderboardResponse(
            period=period,
            metric=metric,
            table=table,
            scatter=scatter,
        )
