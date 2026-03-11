from fastapi import APIRouter

from app.infrastructure.telemetry.logger import get_logger

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health")
def health_check():
    logger.info("health_check_ping")
    return {"status": "healthy"}
