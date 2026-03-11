from fastapi import APIRouter

from app.infrastructure.telemetry.logger import get_logger

router = APIRouter(tags=["health"])
logger = get_logger(__name__).bind(route="/health", surface="api")


@router.get("/health")
def health_check():
    logger.bind(operation="health_check").info("completed", status="healthy")
    return {"status": "healthy"}
