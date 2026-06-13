import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class InsulinEvent(Base):
    __tablename__ = "insulin_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    food_event_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("food_events.id"), nullable=True
    )
    dose: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    injected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
