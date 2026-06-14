#!/usr/bin/env python3
"""Inspect PostgreSQL table counts and sample rows (no PII by default)."""

from __future__ import annotations

import argparse
import asyncio
import sys

from sqlalchemy import func, select
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

TABLES = [
    ("users", User),
    ("food_events", FoodEvent),
    ("insulin_events", InsulinEvent),
    ("dialogs", Dialog),
    ("dialog_requests", DialogRequest),
    ("photo_analyses", PhotoAnalysis),
    ("progress_snapshots", ProgressSnapshot),
    ("recommendations", Recommendation),
    ("consultations", Consultation),
]

SAMPLE_LIMIT = 3
DESC_TRUNCATE = 40


async def count_rows(session: AsyncSession, model) -> int:
    result = await session.scalar(select(func.count()).select_from(model))
    return int(result or 0)


async def print_counts(session: AsyncSession) -> None:
    print("=== Table counts ===")
    for name, model in TABLES:
        count = await count_rows(session, model)
        print(f"  {name}: {count}")


async def print_user_samples(session: AsyncSession, *, verbose: bool) -> None:
    print("\n=== users (sample) ===")
    result = await session.execute(select(User).limit(SAMPLE_LIMIT))
    for user in result.scalars():
        if verbose:
            print(
                f"  id={user.id} telegram_id={user.telegram_id} "
                f"role={user.role} active={user.is_active}"
            )
        else:
            print(
                f"  id={user.id} role={user.role} active={user.is_active} "
                f"display_name={user.display_name!r}"
            )


async def print_food_samples(session: AsyncSession, *, verbose: bool) -> None:
    print("\n=== food_events (sample) ===")
    result = await session.execute(select(FoodEvent).limit(SAMPLE_LIMIT))
    for event in result.scalars():
        if verbose:
            desc = event.description[:DESC_TRUNCATE]
            if len(event.description) > DESC_TRUNCATE:
                desc += "…"
            print(
                f"  id={event.id} user_id={event.user_id} xe={event.xe} "
                f"recorded_at={event.recorded_at.isoformat()} desc={desc!r}"
            )
        else:
            print(
                f"  id={event.id} user_id={event.user_id} xe={event.xe} "
                f"recorded_at={event.recorded_at.isoformat()}"
            )


async def print_insulin_samples(session: AsyncSession, *, verbose: bool) -> None:
    print("\n=== insulin_events (sample) ===")
    result = await session.execute(select(InsulinEvent).limit(SAMPLE_LIMIT))
    for event in result.scalars():
        if verbose:
            comment = event.comment
            if comment and len(comment) > DESC_TRUNCATE:
                comment = comment[:DESC_TRUNCATE] + "…"
            print(
                f"  id={event.id} user_id={event.user_id} dose={event.dose} "
                f"injected_at={event.injected_at.isoformat()} comment={comment!r}"
            )
        else:
            print(
                f"  id={event.id} user_id={event.user_id} dose={event.dose} "
                f"injected_at={event.injected_at.isoformat()}"
            )


async def run_inspect(*, verbose: bool) -> int:
    settings = get_settings()
    if not settings.database_url:
        print("DATABASE_URL is required (see .env.example)", file=sys.stderr)
        return 1

    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with session_factory() as session:
            await print_counts(session)
            await print_user_samples(session, verbose=verbose)
            await print_food_samples(session, verbose=verbose)
            await print_insulin_samples(session, verbose=verbose)
    except Exception as exc:
        print(f"Database error: {exc}", file=sys.stderr)
        return 1
    finally:
        await engine.dispose()

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect PostgreSQL seed data")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show telegram_id and truncated descriptions/comments",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sys.exit(asyncio.run(run_inspect(verbose=args.verbose)))


if __name__ == "__main__":
    main()
