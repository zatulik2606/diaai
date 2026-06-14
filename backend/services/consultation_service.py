from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.consultation import Consultation
from backend.repositories.consultation import ConsultationRepository


class ConsultationService:
    def __init__(self, session: AsyncSession) -> None:
        self._consultations = ConsultationRepository(session)

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
        return await self._consultations.create(
            diabetic_id=diabetic_id,
            doctor_id=doctor_id,
            format=format,
            scheduled_at=scheduled_at,
            status=status,
            doctor_comment=doctor_comment,
        )

    async def list_for_diabetic(self, diabetic_id: uuid.UUID) -> list[Consultation]:
        return await self._consultations.list_by_diabetic(diabetic_id)

    async def list_for_doctor(self, doctor_id: uuid.UUID) -> list[Consultation]:
        return await self._consultations.list_by_doctor(doctor_id)
