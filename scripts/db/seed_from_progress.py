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
from datetime import date, datetime
from pathlib import Path

from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.config import get_settings
from backend.models.consultation import Consultation
from backend.models.dialog import Dialog
from backend.models.food_event import FoodEvent
from backend.models.insulin_event import InsulinEvent
from backend.models.photo_analysis import PhotoAnalysis
from backend.models.progress_snapshot import ProgressSnapshot
from backend.models.recommendation import Recommendation
from backend.models.request import DialogRequest
from backend.models.user import User

DEFAULT_IMPORT = Path("data/progress-import.v1.json")


class UserImport(BaseModel):
    id: uuid.UUID
    telegram_id: int | None = None
    telegram_username: str | None = None
    role: str
    display_name: str | None = None
    email: str | None = None
    is_active: bool = True


class DialogImport(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    channel: str = "telegram"
    status: str = "active"


class DialogRequestImport(BaseModel):
    id: uuid.UUID
    dialog_id: uuid.UUID
    user_id: uuid.UUID
    type: str
    content: str | None = None
    reply: str
    media: dict | None = None
    created_at: datetime


class PhotoAnalysisImport(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    request_id: uuid.UUID
    food_event_id: uuid.UUID | None = None
    object_type: str
    xe: float | None = None
    bje: float | None = None
    proteins: float | None = None
    fats: float | None = None
    carbs: float | None = None
    confidence: float | None = None
    comment: str | None = None
    created_at: datetime | None = None


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


class ProgressSnapshotImport(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    period: str
    period_start: date
    period_end: date
    sum_xe: float
    sum_bje: float
    sum_insulin: float
    trend: str
    sum_proteins: float | None = None
    sum_fats: float | None = None
    sum_carbs: float | None = None
    comment: str | None = None


class ConsultationImport(BaseModel):
    id: uuid.UUID
    diabetic_id: uuid.UUID
    doctor_id: uuid.UUID
    format: str
    scheduled_at: datetime
    status: str
    doctor_comment: str | None = None


class ProgressImport(BaseModel):
    schema_version: int = Field(ge=1)
    users: list[UserImport]
    dialogs: list[DialogImport] = Field(default_factory=list)
    dialog_requests: list[DialogRequestImport] = Field(default_factory=list)
    food_events: list[FoodEventImport]
    insulin_events: list[InsulinEventImport]
    progress_snapshots: list[ProgressSnapshotImport] = Field(default_factory=list)
    consultations: list[ConsultationImport] = Field(default_factory=list)
    recommendations: list[dict] = Field(default_factory=list)
    photo_analyses: list[PhotoAnalysisImport] = Field(default_factory=list)


def load_import(path: Path) -> ProgressImport:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return ProgressImport.model_validate(raw)


def validate_references(data: ProgressImport) -> None:
    user_ids = {u.id for u in data.users}
    food_ids = {f.id for f in data.food_events}
    dialog_ids = {d.id for d in data.dialogs}
    request_ids = {r.id for r in data.dialog_requests}

    for event in data.food_events:
        if event.user_id not in user_ids:
            msg = f"food_event {event.id}: unknown user_id {event.user_id}"
            raise ValueError(msg)
        if event.request_id is not None and event.request_id not in request_ids:
            msg = f"food_event {event.id}: unknown request_id {event.request_id}"
            raise ValueError(msg)

    for event in data.insulin_events:
        if event.user_id not in user_ids:
            msg = f"insulin_event {event.id}: unknown user_id {event.user_id}"
            raise ValueError(msg)
        if event.food_event_id is not None and event.food_event_id not in food_ids:
            msg = f"insulin_event {event.id}: unknown food_event_id {event.food_event_id}"
            raise ValueError(msg)

    for snapshot in data.progress_snapshots:
        if snapshot.user_id not in user_ids:
            msg = f"progress_snapshot {snapshot.id}: unknown user_id {snapshot.user_id}"
            raise ValueError(msg)

    for consultation in data.consultations:
        if consultation.diabetic_id not in user_ids:
            msg = f"consultation {consultation.id}: unknown diabetic_id"
            raise ValueError(msg)
        if consultation.doctor_id not in user_ids:
            msg = f"consultation {consultation.id}: unknown doctor_id"
            raise ValueError(msg)

    for dialog in data.dialogs:
        if dialog.user_id not in user_ids:
            msg = f"dialog {dialog.id}: unknown user_id {dialog.user_id}"
            raise ValueError(msg)

    for request in data.dialog_requests:
        if request.user_id not in user_ids:
            msg = f"dialog_request {request.id}: unknown user_id"
            raise ValueError(msg)
        if request.dialog_id not in dialog_ids:
            msg = f"dialog_request {request.id}: unknown dialog_id"
            raise ValueError(msg)

    for photo in data.photo_analyses:
        if photo.user_id not in user_ids:
            msg = f"photo_analysis {photo.id}: unknown user_id"
            raise ValueError(msg)
        if photo.request_id not in request_ids:
            msg = f"photo_analysis {photo.id}: unknown request_id"
            raise ValueError(msg)
        if photo.food_event_id is not None and photo.food_event_id not in food_ids:
            msg = f"photo_analysis {photo.id}: unknown food_event_id"
            raise ValueError(msg)


async def upsert_rows(session: AsyncSession, table, rows: list[dict]) -> int:
    if not rows:
        return 0
    stmt = insert(table).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount or 0


async def seed(session: AsyncSession, data: ProgressImport) -> dict[str, int]:
    counts = {}
    counts["users"] = await upsert_rows(
        session, User.__table__, [u.model_dump() for u in data.users]
    )
    counts["dialogs"] = await upsert_rows(
        session, Dialog.__table__, [d.model_dump() for d in data.dialogs]
    )
    counts["dialog_requests"] = await upsert_rows(
        session,
        DialogRequest.__table__,
        [r.model_dump() for r in data.dialog_requests],
    )
    counts["food_events"] = await upsert_rows(
        session, FoodEvent.__table__, [f.model_dump() for f in data.food_events]
    )
    counts["insulin_events"] = await upsert_rows(
        session, InsulinEvent.__table__, [i.model_dump() for i in data.insulin_events]
    )
    counts["progress_snapshots"] = await upsert_rows(
        session,
        ProgressSnapshot.__table__,
        [s.model_dump() for s in data.progress_snapshots],
    )
    counts["consultations"] = await upsert_rows(
        session,
        Consultation.__table__,
        [c.model_dump() for c in data.consultations],
    )
    if data.recommendations:
        counts["recommendations"] = await upsert_rows(
            session, Recommendation.__table__, data.recommendations
        )
    counts["photo_analyses"] = await upsert_rows(
        session,
        PhotoAnalysis.__table__,
        [p.model_dump(exclude_none=True) for p in data.photo_analyses],
    )
    return counts


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
            counts = await seed(session, data)
    except Exception as exc:
        print(f"Database error: {exc}", file=sys.stderr)
        return 1
    finally:
        await engine.dispose()

    parts = ", ".join(f"{k} +{v}" for k, v in counts.items())
    print(f"Seed complete: {parts} (skipped rows already present)")
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
