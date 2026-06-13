import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class FoodEvent(Base):
    __tablename__ = "food_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    request_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("dialog_requests.id"), nullable=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    xe: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    bje: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    proteins: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    fats: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    carbs: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
