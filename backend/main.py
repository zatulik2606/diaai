import asyncio
import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from backend.api.v1.router import api_router
from backend.config import get_settings, validate_service_token
from backend.database import dispose_db, init_db
from backend.debug_glitchtip import include_debug_routes
from backend.glitchtip_poller import start_glitchtip_poller
from backend.glitchtip_webhook import include_glitchtip_webhook
from backend.exceptions import AppError
from backend.health import router as health_router
from backend.metrics import setup_metrics
from backend.schemas.errors import ErrorBody, ErrorDetail
from backend.sentry_setup import init_sentry

logger = logging.getLogger(__name__)

init_sentry(get_settings())


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    validate_service_token(settings)
    poller_task = start_glitchtip_poller(settings)
    if settings.database_url:
        init_db(settings.database_url)
        logger.info("Backend startup (database configured)")
    else:
        logger.warning("Backend startup without DATABASE_URL")
    try:
        yield
    finally:
        if poller_task is not None:
            poller_task.cancel()
            try:
                await poller_task
            except asyncio.CancelledError:
                pass
    await dispose_db()
    logger.info("Backend shutdown")


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-Id") or str(uuid4())
        request.state.request_id = request_id
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-Id"] = request_id
        logger.info(
            "request_id=%s method=%s path=%s status=%s duration_ms=%.1f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


def _error_response(exc: AppError) -> JSONResponse:
    body = ErrorBody(error=ErrorDetail(code=exc.code, message=exc.message, details=exc.details))
    return JSONResponse(status_code=exc.status_code, content=body.model_dump(exclude_none=True))


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level.upper())

    app = FastAPI(
        title="diaai Backend API",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(RequestIdMiddleware)

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        if exc.status_code >= 500:
            logger.warning(
                "request_id=%s error_code=%s status=%s",
                request_id,
                exc.code,
                exc.status_code,
            )
        return _error_response(exc)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": jsonable_encoder(exc.errors())})

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.warning(
            "request_id=%s unhandled_error=%s",
            request_id,
            exc.__class__.__name__,
        )
        if get_settings().glitchtip_dsn:
            import sentry_sdk

            sentry_sdk.set_tag("request_id", request_id)
            sentry_sdk.capture_exception(exc)
        return _error_response(
            AppError(
                code="INTERNAL_ERROR",
                message="Internal server error",
                status_code=500,
            )
        )

    app.include_router(health_router)
    app.include_router(api_router, prefix="/api/v1")
    include_debug_routes(app, settings)
    include_glitchtip_webhook(app, settings)
    setup_metrics(app)
    return app


app = create_app()
