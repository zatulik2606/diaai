from fastapi import Depends, HTTPException, Query
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


async def require_leaderboard_viewer(
    doctor_telegram_id: int | None = Query(default=None),
    patient_telegram_id: int | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if doctor_telegram_id is not None:
        return await UserRepository(db).require_doctor(doctor_telegram_id)
    if patient_telegram_id is not None:
        return await UserRepository(db).require_diabetic(patient_telegram_id)
    raise HTTPException(
        status_code=422,
        detail="doctor_telegram_id or patient_telegram_id is required",
    )
