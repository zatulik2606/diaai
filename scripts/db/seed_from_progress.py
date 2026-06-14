#!/usr/bin/env python3
"""Load progress-import JSON into PostgreSQL (idempotent by primary key).

Uses INSERT ... ON CONFLICT (id) DO NOTHING — safe to run multiple times.
Does not log message text, descriptions, or telegram_id (project conventions).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field, field_validator
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.config import get_settings
from backend.models.food_event import FoodEvent
from backend.models.insulin_event import InsulinEvent
from backend.models.user import User

DEFAULT_IMPORT = Path("data/progress-import.v1.json")


class UserImport(BaseModel):
    id: uuid.UUID
    telegram_id: int
    role: str
    is_active: bool = True


class FoodEventImport(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    request_id: uuid.UUID | None = None
    description: str
    xe: float
    bje: float
    proteins: float | None = None
    fats: float | None = None
    carbs: float | None = None
    source: str
    comment: str | None = None
    recorded_at: datetime


class InsulinEventImport(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    food_event_id: uuid.UUID | None = None
    dose: float
    injected_at: datetime
    comment: str | None = None


class ProgressImport(BaseModel):
    schema_version: int = Field(ge=1)
    users: list[UserImport]
    food_events: list[FoodEventImport]
    insulin_events: list[InsulinEventImport]
    progress_snapshots: list[dict] = Field(default_factory=list)

    @field_validator("progress_snapshots")
    @classmethod
    def warn_unsupported_snapshots(cls, value: list[dict]) -> list[dict]:
        if value:
            print(
                "Note: progress_snapshots in import file are ignored until migration 002 (iter 5).",
                file=sys.stderr,
            )
        return value


def load_import(path: Path) -> ProgressImport:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return ProgressImport.model_validate(raw)


def validate_references(data: ProgressImport) -> None:
    user_ids = {u.id for u in data.users}
    food_ids = {f.id for f in data.food_events}

    for event in data.food_events:
        if event.user_id not in user_ids:
            msg = f"food_event {event.id}: unknown user_id {event.user_id}"
            raise ValueError(msg)

    for event in data.insulin_events:
        if event.user_id not in user_ids:
            msg = f"insulin_event {event.id}: unknown user_id {event.user_id}"
            raise ValueError(msg)
        if event.food_event_id is not None and event.food_event_id not in food_ids:
            msg = f"insulin_event {event.id}: unknown food_event_id {event.food_event_id}"
            raise ValueError(msg)


async def upsert_rows(session: AsyncSession, table, rows: list[dict]) -> int:
    if not rows:
        return 0
    stmt = insert(table).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount or 0


async def seed(session: AsyncSession, data: ProgressImport) -> tuple[int, int, int]:
    users_inserted = await upsert_rows(
        session,
        User.__table__,
        [u.model_dump() for u in data.users],
    )
    food_inserted = await upsert_rows(
        session,
        FoodEvent.__table__,
        [f.model_dump() for f in data.food_events],
    )
    insulin_inserted = await upsert_rows(
        session,
        InsulinEvent.__table__,
        [i.model_dump() for i in data.insulin_events],
    )
    return users_inserted, food_inserted, insulin_inserted


async def run_seed(path: Path) -> int:
    settings = get_settings()
    if not settings.database_url:
        print("DATABASE_URL is required (see .env.example)", file=sys.stderr)
        return 1

    try:
        data = load_import(path)
        validate_references(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Import error: {exc}", file=sys.stderr)
        return 1

    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with session_factory() as session:
            users_n, food_n, insulin_n = await seed(session, data)
    except Exception as exc:
        print(f"Database error: {exc}", file=sys.stderr)
        return 1
    finally:
        await engine.dispose()

    print(
        f"Seed complete: users +{users_n}, food_events +{food_n}, insulin_events +{insulin_n} "
        f"(skipped rows already present)"
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load progress-import JSON into PostgreSQL")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_IMPORT,
        help=f"Import file (default: {DEFAULT_IMPORT})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.file.is_file():
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    sys.exit(asyncio.run(run_seed(args.file)))


if __name__ == "__main__":
    main()
