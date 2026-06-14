import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class PhotoAnalysis(Base):
    __tablename__ = "photo_analyses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    request_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dialog_requests.id"), nullable=False, index=True
    )
    food_event_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("food_events.id"), nullable=True
    )
    object_type: Mapped[str] = mapped_column(Text, nullable=False)
    xe: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    bje: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    proteins: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    fats: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    carbs: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
