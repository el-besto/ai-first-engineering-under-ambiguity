import uuid

from fastapi import FastAPI, Request

from app.infrastructure.telemetry.logger import (
    bind_context,
    clear_context,
    configure_logging,
    get_logger,
)
from drivers.api.config import APIConfig
from drivers.api.routes.health import router as health_router
from drivers.api.routes.triage import router as triage_router

# Initialize logging based on environment
config = APIConfig()
configure_logging(
    environment=config.environment,
    log_level=config.log_level,
    log_format=config.log_format,
)
logger = get_logger(__name__)

app = FastAPI()

app.include_router(health_router)
app.include_router(triage_router)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # Generates a new trace_id for each request or uses an incoming one
    trace_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    bind_context(trace_id=trace_id, path=request.url.path, method=request.method)

    logger.info("request_started")
    try:
        response = await call_next(request)
        logger.info("request_completed", status_code=response.status_code)
        # Optionally add the trace_id to response headers
        response.headers["X-Request-ID"] = trace_id
        return response
    except Exception as e:
        logger.exception("request_failed", error=str(e))
        raise
    finally:
        clear_context()
