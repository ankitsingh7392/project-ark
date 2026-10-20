"""FastAPI entrypoint. Only /health exists until the golden set is built (docs/brief.md)."""

import uuid
from collections.abc import Awaitable, Callable

import structlog
from fastapi import FastAPI, Request, Response

from app import __version__
from app.config import settings
from app.schemas import HealthResponse

log = structlog.get_logger()

app = FastAPI(title="FinRAG", version=__version__)


@app.middleware("http")
async def request_id_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    structlog.contextvars.unbind_contextvars("request_id")
    return response


def _db_status() -> str:
    if not settings.database_url:
        return "not_configured"
    try:
        import psycopg

        with psycopg.connect(
            settings.database_url, connect_timeout=settings.db_health_timeout_s
        ) as c:
            c.execute("select 1")
        return "up"
    except Exception as exc:  # noqa: BLE001 — health must never raise
        log.warning("db_health_failed", exc_type=type(exc).__name__)
        return "down"


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    db = _db_status()
    status = "ok" if db in ("up", "not_configured") else "degraded"
    return HealthResponse(status=status, version=__version__, db=db)  # type: ignore[arg-type]
