import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.consultation import Consultation


class ConsultationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, consultation_id: uuid.UUID) -> Consultation | None:
        return await self._session.get(Consultation, consultation_id)

    async def create(
        self,
        *,
        diabetic_id: uuid.UUID,
        doctor_id: uuid.UUID,
        format: str,
        scheduled_at: datetime,
        status: str = "scheduled",
        doctor_comment: str | None = None,
    ) -> Consultation:
        consultation = Consultation(
            diabetic_id=diabetic_id,
            doctor_id=doctor_id,
            format=format,
            scheduled_at=scheduled_at,
            status=status,
            doctor_comment=doctor_comment,
        )
        self._session.add(consultation)
        await self._session.flush()
        return consultation

    async def list_by_diabetic(self, diabetic_id: uuid.UUID) -> list[Consultation]:
        result = await self._session.execute(
            select(Consultation)
            .where(Consultation.diabetic_id == diabetic_id)
            .order_by(Consultation.scheduled_at.desc())
        )
        return list(result.scalars().all())

    async def list_by_doctor(self, doctor_id: uuid.UUID) -> list[Consultation]:
        result = await self._session.execute(
            select(Consultation)
            .where(Consultation.doctor_id == doctor_id)
            .order_by(Consultation.scheduled_at.desc())
        )
        return list(result.scalars().all())
