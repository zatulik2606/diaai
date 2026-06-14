from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.api.deps import verify_service_token
from backend.api.v1.web.deps import require_diabetic
from backend.api.v1.web.service_deps import get_web_patient_service
from backend.models.user import User
from backend.schemas.web import (
    DashboardActivityResponse,
    MatrixPeriod,
    PaginatedPatientQuestionsResponse,
    PaginatedPatientSubmissionsResponse,
    PatientDashboardSummaryResponse,
    PatientProgressMatrixResponse,
)
from backend.services.web_patient_service import WebPatientService
from backend.services.web_utils import clamp_limit, clamp_offset

router = APIRouter(prefix="/patient/dashboard", tags=["web"])

LimitParam = Annotated[int, Query(ge=1, le=100, description="Page size (max 100)")]
OffsetParam = Annotated[int, Query(ge=0)]


@router.get("/summary", response_model=PatientDashboardSummaryResponse)
async def patient_dashboard_summary(
    patient: User = Depends(require_diabetic),
    period_days: int = Query(default=7, ge=1, le=365),
    _: None = Depends(verify_service_token),
    service: WebPatientService = Depends(get_web_patient_service),
) -> PatientDashboardSummaryResponse:
    return await service.get_summary(patient, period_days=period_days)


@router.get("/activity", response_model=DashboardActivityResponse)
async def patient_dashboard_activity(
    patient: User = Depends(require_diabetic),
    days: int = Query(default=14, ge=1, le=90),
    _: None = Depends(verify_service_token),
    service: WebPatientService = Depends(get_web_patient_service),
) -> DashboardActivityResponse:
    return await service.get_activity(patient, days=days)


@router.get("/questions", response_model=PaginatedPatientQuestionsResponse)
async def patient_dashboard_questions(
    patient: User = Depends(require_diabetic),
    limit: LimitParam = 20,
    offset: OffsetParam = 0,
    _: None = Depends(verify_service_token),
    service: WebPatientService = Depends(get_web_patient_service),
) -> PaginatedPatientQuestionsResponse:
    return await service.get_questions(
        patient,
        limit=clamp_limit(limit),
        offset=clamp_offset(offset),
    )


@router.get("/submissions", response_model=PaginatedPatientSubmissionsResponse)
async def patient_dashboard_submissions(
    patient: User = Depends(require_diabetic),
    limit: LimitParam = 20,
    offset: OffsetParam = 0,
    _: None = Depends(verify_service_token),
    service: WebPatientService = Depends(get_web_patient_service),
) -> PaginatedPatientSubmissionsResponse:
    return await service.get_submissions(
        patient,
        limit=clamp_limit(limit),
        offset=clamp_offset(offset),
    )


@router.get("/progress-matrix", response_model=PatientProgressMatrixResponse)
async def patient_dashboard_progress_matrix(
    patient: User = Depends(require_diabetic),
    period: MatrixPeriod = Query(default="week"),
    _: None = Depends(verify_service_token),
    service: WebPatientService = Depends(get_web_patient_service),
) -> PatientProgressMatrixResponse:
    return await service.get_progress_matrix(patient, period=period)
