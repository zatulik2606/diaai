import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    period: Mapped[str] = mapped_column(Text, nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    sum_xe: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    sum_bje: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    sum_insulin: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    sum_proteins: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    sum_fats: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    sum_carbs: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    trend: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
