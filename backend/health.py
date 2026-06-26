import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from backend import database

logger = logging.getLogger(__name__)

router = APIRouter(tags=["system"])


async def probe_database() -> bool:
    if database.AsyncSessionLocal is None:
        return False
    try:
        async with database.AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.warning("Health check: database probe failed", exc_info=True)
        return False


@router.get("/health")
async def health(request: Request) -> JSONResponse:
    version = request.app.version
    if await probe_database():
        return JSONResponse(
            content={"status": "ok", "version": version, "database": "ok"},
        )
    return JSONResponse(
        status_code=503,
        content={"status": "unavailable", "database": "down"},
    )
