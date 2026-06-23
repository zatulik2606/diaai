from __future__ import annotations

import re
import uuid

import sqlglot
from sqlglot import exp

from backend.exceptions import AppError

ALLOWED_TABLES = frozenset(
    {
        "users",
        "food_events",
        "insulin_events",
        "progress_snapshots",
        "dialog_requests",
        "photo_analyses",
    }
)

FORBIDDEN_KEYWORDS = frozenset(
    {
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke",
        "execute",
        "copy",
        "pg_catalog",
        "information_schema",
    }
)


class SqlGuard:
    def __init__(self, max_row_limit: int = 100) -> None:
        self._max_row_limit = max_row_limit

    def validate_and_enforce(self, sql: str, *, dialect: str = "postgres") -> str:
        cleaned = self._strip_sql(sql)
        if not cleaned:
            raise AppError(
                code="INVALID_SQL",
                message="Empty SQL query",
                status_code=422,
            )

        lowered = cleaned.lower()
        if ";" in cleaned.rstrip(";"):
            raise AppError(
                code="INVALID_SQL",
                message="Multiple SQL statements are not allowed",
                status_code=422,
            )

        for keyword in FORBIDDEN_KEYWORDS:
            if re.search(rf"\b{keyword}\b", lowered):
                raise AppError(
                    code="INVALID_SQL",
                    message="Query contains forbidden keywords",
                    status_code=422,
                )

        try:
            expression = sqlglot.parse_one(cleaned, read=dialect)
        except sqlglot.errors.ParseError as exc:
            raise AppError(
                code="INVALID_SQL",
                message="Could not parse SQL query",
                status_code=422,
            ) from exc

        if not isinstance(expression, exp.Select):
            raise AppError(
                code="INVALID_SQL",
                message="Only SELECT queries are allowed",
                status_code=422,
            )

        tables = {table.name.lower() for table in expression.find_all(exp.Table)}
        unknown = tables - ALLOWED_TABLES
        if unknown:
            raise AppError(
                code="INVALID_SQL",
                message="Query references disallowed tables",
                status_code=422,
            )

        return self._enforce_limit(expression, dialect=dialect)

    def assert_diabetic_scope(
        self,
        sql: str,
        user_id: uuid.UUID,
        *,
        telegram_id: int | None = None,
    ) -> None:
        lowered = sql.lower()
        uid = str(user_id).lower()
        if uid in lowered:
            return
        if telegram_id is not None and str(telegram_id) in lowered:
            return
        raise AppError(
            code="SCOPE_VIOLATION",
            message="Query must be scoped to the current patient",
            status_code=403,
        )

    @staticmethod
    def _strip_sql(raw: str) -> str:
        text = raw.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:sql)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
        return text.strip().rstrip(";")

    def _enforce_limit(self, expression: exp.Select, *, dialect: str) -> str:
        limit_node = expression.args.get("limit")
        if limit_node is None:
            limited = expression.limit(self._max_row_limit)
            return limited.sql(dialect=dialect)

        try:
            limit_value = int(limit_node.expression.this)
        except (AttributeError, TypeError, ValueError) as exc:
            raise AppError(
                code="INVALID_SQL",
                message="Invalid LIMIT clause",
                status_code=422,
            ) from exc

        if limit_value > self._max_row_limit:
            raise AppError(
                code="INVALID_SQL",
                message=f"LIMIT must be at most {self._max_row_limit}",
                status_code=422,
            )

        return expression.sql(dialect=dialect)
