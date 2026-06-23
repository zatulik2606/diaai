from __future__ import annotations

import asyncio
import logging
import uuid
from decimal import Decimal
from pathlib import Path
from typing import Any

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import Settings, get_settings
from backend.database import get_db
from backend.exceptions import AppError
from backend.models.user import User
from backend.schemas.analytics_query import AnalyticsQueryResponse, ChartHint
from backend.services.llm_service import LlmService
from backend.services.sql_guard import SqlGuard

logger = logging.getLogger(__name__)

_ANALYTICS_PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "analytics_sql.txt"


def load_analytics_sql_prompt() -> str:
    return _ANALYTICS_PROMPT_PATH.read_text(encoding="utf-8").strip()


class AnalyticsQueryService:
    def __init__(
        self,
        db: AsyncSession,
        llm_service: LlmService,
        *,
        sql_guard: SqlGuard,
        query_timeout_seconds: float,
        llm_timeout_seconds: float,
    ) -> None:
        self._db = db
        self._llm = llm_service
        self._guard = sql_guard
        self._query_timeout = query_timeout_seconds
        self._llm_timeout = llm_timeout_seconds

    async def query(self, viewer: User, question: str) -> AnalyticsQueryResponse:
        cleaned = question.strip()
        if not cleaned:
            raise AppError(
                code="BAD_REQUEST",
                message="Question must not be empty",
                status_code=422,
            )

        sql = await self._generate_sql(viewer, cleaned)
        sql = self._guard.validate_and_enforce(sql)
        if viewer.role == "diabetic":
            self._guard.assert_diabetic_scope(
                sql,
                viewer.id,
                telegram_id=viewer.telegram_id,
            )

        columns, rows = await self._execute(sql)
        answer = self._format_answer(cleaned, columns, rows)
        chart_hint = self._infer_chart_hint(columns, rows)
        serializable_rows = [[self._serialize_cell(cell) for cell in row] for row in rows]

        return AnalyticsQueryResponse(
            answer=answer,
            columns=columns,
            rows=serializable_rows,
            chart_hint=chart_hint,
        )

    async def _generate_sql(self, viewer: User, question: str) -> str:
        context = f"Роль: {viewer.role}.\nuser_id текущего пользователя: {viewer.id}.\n"
        if viewer.role == "diabetic":
            context += "Обязательно фильтруй все таблицы с user_id по этому UUID.\n"
        else:
            context += "Доктор может запрашивать данные по всем пациентам (role=diabetic).\n"

        user_message = f"{context}\nВопрос: {question}"
        system_prompt = load_analytics_sql_prompt()

        try:
            raw_sql = await asyncio.wait_for(
                asyncio.to_thread(
                    self._llm.generate_reply,
                    system_prompt,
                    [],
                    user_message,
                ),
                timeout=self._llm_timeout,
            )
        except TimeoutError as exc:
            raise AppError(
                code="ANALYTICS_UNAVAILABLE",
                message="Analytics query timed out",
                status_code=504,
            ) from exc

        return raw_sql.strip()

    async def _execute(self, sql: str) -> tuple[list[str], list[tuple[Any, ...]]]:
        try:
            result = await asyncio.wait_for(
                self._db.execute(text(sql)),
                timeout=self._query_timeout,
            )
        except TimeoutError as exc:
            raise AppError(
                code="QUERY_TIMEOUT",
                message="Database query timed out",
                status_code=504,
            ) from exc
        except Exception as exc:  # noqa: BLE001
            logger.warning("Analytics SQL execution failed: %s", exc.__class__.__name__)
            raise AppError(
                code="QUERY_FAILED",
                message="Could not execute analytics query",
                status_code=422,
            ) from exc

        rows = result.fetchall()
        columns = list(result.keys())
        return columns, [tuple(row) for row in rows]

    @staticmethod
    def _serialize_cell(value: Any) -> str | int | float | None:
        if value is None:
            return None
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, uuid.UUID):
            return str(value)
        if isinstance(value, (str, int, float, bool)):
            if isinstance(value, bool):
                return str(value)
            return value
        return str(value)

    @staticmethod
    def _format_answer(
        question: str,
        columns: list[str],
        rows: list[tuple[Any, ...]],
    ) -> str:
        if not rows:
            return "По вашему запросу данных не найдено. Проверьте имя пациента или период."

        if len(rows) == 1 and len(columns) == 1:
            value = AnalyticsQueryService._serialize_cell(rows[0][0])
            return f"Результат: {value}."

        if len(columns) == 2 and len(rows) <= 10:
            lines = [
                f"{AnalyticsQueryService._serialize_cell(row[0])}: "
                f"{AnalyticsQueryService._serialize_cell(row[1])}"
                for row in rows
            ]
            return "Результаты:\n" + "\n".join(lines)

        return f"Найдено записей: {len(rows)}. Подробности — в таблице ниже."

    @staticmethod
    def _infer_chart_hint(columns: list[str], rows: list[tuple[Any, ...]]) -> ChartHint:
        if not rows:
            return "table"
        if len(rows) == 1 and len(columns) == 1:
            return "scalar"
        if len(columns) >= 2:
            second_is_numeric = all(
                isinstance(row[1], (int, float, Decimal)) or row[1] is None for row in rows
            )
            if second_is_numeric and len(rows) <= 20:
                return "bar"
        date_markers = ("date", "day", "recorded", "period")
        if any(any(marker in col.lower() for marker in date_markers) for col in columns):
            return "line"
        return "table"


def get_analytics_query_service(
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> AnalyticsQueryService:
    llm_service = LlmService(
        api_key=settings.openrouter_api_key,
        model=settings.analytics_query_model,
        timeout_seconds=settings.analytics_query_llm_timeout_seconds,
    )
    return AnalyticsQueryService(
        db,
        llm_service,
        sql_guard=SqlGuard(max_row_limit=settings.analytics_query_row_limit),
        query_timeout_seconds=settings.analytics_query_timeout_seconds,
        llm_timeout_seconds=settings.analytics_query_llm_timeout_seconds,
    )
