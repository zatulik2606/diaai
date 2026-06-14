"""Nine-table metadata after migration 002 models."""

from backend.database import Base
from backend.models import (  # noqa: F401
    Consultation,
    Dialog,
    DialogRequest,
    FoodEvent,
    InsulinEvent,
    PhotoAnalysis,
    ProgressSnapshot,
    Recommendation,
    User,
)

EXPECTED_TABLES = {
    "users",
    "dialogs",
    "dialog_requests",
    "food_events",
    "insulin_events",
    "photo_analyses",
    "progress_snapshots",
    "recommendations",
    "consultations",
}


def test_metadata_has_nine_tables() -> None:
    assert EXPECTED_TABLES <= set(Base.metadata.tables.keys())
