import uuid

from fastapi import FastAPI, Request

from app.infrastructure.telemetry.logger import (
    bind_context,
    clear_context,
    configure_logging,
    get_logger,
    log_exception,
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
logger = get_logger(__name__).bind(driver="FastAPI", surface="api")

app = FastAPI()

app.include_router(health_router)
app.include_router(triage_router)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # Reuse an incoming request ID when present so logs and responses share one correlation key.
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    clear_context()
    bind_context(request_id=request_id, path=request.url.path, method=request.method, surface="api")
    log = logger.bind(operation="http_request")
    log.info("started")
    try:
        response = await call_next(request)
        log.info("completed", status_code=response.status_code)
        # Echo the request ID back to the caller for correlation.
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as e:
        log_exception(log, "failed", e)
        raise
    finally:
        clear_context()
