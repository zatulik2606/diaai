from fastapi import APIRouter

from backend.api.v1.web import assistant_history, auth, doctor_dashboard, leaderboard

router = APIRouter(prefix="/web")
router.include_router(auth.router)
router.include_router(doctor_dashboard.router)
router.include_router(leaderboard.router)
router.include_router(assistant_history.router)
