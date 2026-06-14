from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.services.web_auth_service import WebAuthService
from backend.services.web_chat_service import WebChatService
from backend.services.web_doctor_service import WebDoctorService
from backend.services.web_leaderboard_service import WebLeaderboardService
from backend.services.web_patient_service import WebPatientService


def get_web_auth_service(db: AsyncSession = Depends(get_db)) -> WebAuthService:
    return WebAuthService(db)


def get_web_doctor_service(db: AsyncSession = Depends(get_db)) -> WebDoctorService:
    return WebDoctorService(db)


def get_web_leaderboard_service(db: AsyncSession = Depends(get_db)) -> WebLeaderboardService:
    return WebLeaderboardService(db)


def get_web_patient_service(db: AsyncSession = Depends(get_db)) -> WebPatientService:
    return WebPatientService(db)


def get_web_chat_service(db: AsyncSession = Depends(get_db)) -> WebChatService:
    return WebChatService(db)
