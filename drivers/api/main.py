import typing
import uuid

from fastapi import Depends, FastAPI, Request
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel

from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.infrastructure.telemetry.logger import (
    bind_context,
    clear_context,
    configure_logging,
    get_logger,
)
from app.interface_adapters.orchestrators.triage_graph_state import (
    TriageGraphState,
    map_state_to_triage_result,
)
from drivers.api.config import APIConfig
from drivers.api.dependencies import get_triage_graph

# Initialize logging based on environment
config = APIConfig()
configure_logging(
    environment=config.environment,
    log_level=config.log_level,
    log_format=config.log_format,
)
logger = get_logger(__name__)

app = FastAPI()


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


class TriageRequest(BaseModel):
    policy_number: str


@app.get("/health")
def health_check():
    logger.info("health_check_ping")
    return {"status": "healthy"}


@app.post("/triage")
def run_triage(
    req: TriageRequest,
    graph: CompiledStateGraph = Depends(get_triage_graph),  # noqa: B008
):
    logger.info("triage_requested", policy_number=req.policy_number)

    # Map strict scenario names to bundle fakes for the PoC
    policy_str = req.policy_number.upper()
    if "MISSING" in policy_str:
        bundle = ClaimIntakeBundle.fake_missing_information()
    elif "AMBIGUOUS" in policy_str:
        bundle = ClaimIntakeBundle.fake_ambiguous()
    else:
        bundle = ClaimIntakeBundle.fake_complete()

    initial_state = {"claim_bundle": bundle}
    # Execute the graph
    result = typing.cast(TriageGraphState, graph.invoke(initial_state))

    return map_state_to_triage_result(result)
