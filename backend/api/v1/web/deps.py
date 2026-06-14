from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.user import User
from backend.repositories.user import UserRepository


async def require_doctor(
    doctor_telegram_id: int,
    db: AsyncSession = Depends(get_db),
) -> User:
    return await UserRepository(db).require_doctor(doctor_telegram_id)


async def require_diabetic(
    patient_telegram_id: int,
    db: AsyncSession = Depends(get_db),
) -> User:
    return await UserRepository(db).require_diabetic(patient_telegram_id)
