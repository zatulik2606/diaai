from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.api.deps import verify_service_token
from backend.api.v1.web.deps import require_doctor
from backend.api.v1.web.service_deps import get_web_doctor_service
from backend.models.user import User
from backend.schemas.web import (
    DashboardActivityResponse,
    DashboardSummaryResponse,
    MatrixPeriod,
    PaginatedQuestionsResponse,
    PaginatedSubmissionsResponse,
    ProgressMatrixResponse,
)
from backend.services.web_doctor_service import WebDoctorService
from backend.services.web_utils import clamp_limit, clamp_offset

router = APIRouter(prefix="/doctor/dashboard", tags=["web"])

LimitParam = Annotated[int, Query(ge=1, le=100, description="Page size (max 100)")]
OffsetParam = Annotated[int, Query(ge=0)]


@router.get("/summary", response_model=DashboardSummaryResponse)
async def dashboard_summary(
    _doctor: User = Depends(require_doctor),
    period_days: int = Query(default=7, ge=1, le=365),
    _: None = Depends(verify_service_token),
    service: WebDoctorService = Depends(get_web_doctor_service),
) -> DashboardSummaryResponse:
    return await service.get_summary(period_days=period_days)


@router.get("/activity", response_model=DashboardActivityResponse)
async def dashboard_activity(
    _doctor: User = Depends(require_doctor),
    days: int = Query(default=14, ge=1, le=90),
    _: None = Depends(verify_service_token),
    service: WebDoctorService = Depends(get_web_doctor_service),
) -> DashboardActivityResponse:
    return await service.get_activity(days=days)


@router.get("/questions", response_model=PaginatedQuestionsResponse)
async def dashboard_questions(
    _doctor: User = Depends(require_doctor),
    limit: LimitParam = 20,
    offset: OffsetParam = 0,
    _: None = Depends(verify_service_token),
    service: WebDoctorService = Depends(get_web_doctor_service),
) -> PaginatedQuestionsResponse:
    return await service.get_questions(
        limit=clamp_limit(limit),
        offset=clamp_offset(offset),
    )


@router.get("/submissions", response_model=PaginatedSubmissionsResponse)
async def dashboard_submissions(
    _doctor: User = Depends(require_doctor),
    limit: LimitParam = 20,
    offset: OffsetParam = 0,
    _: None = Depends(verify_service_token),
    service: WebDoctorService = Depends(get_web_doctor_service),
) -> PaginatedSubmissionsResponse:
    return await service.get_submissions(
        limit=clamp_limit(limit),
        offset=clamp_offset(offset),
    )


@router.get("/progress-matrix", response_model=ProgressMatrixResponse)
async def dashboard_progress_matrix(
    _doctor: User = Depends(require_doctor),
    period: MatrixPeriod = Query(default="week"),
    columns: str = Query(default="period", pattern="^(period|metric)$"),
    _: None = Depends(verify_service_token),
    service: WebDoctorService = Depends(get_web_doctor_service),
) -> ProgressMatrixResponse:
    del columns
    return await service.get_progress_matrix(period=period)
