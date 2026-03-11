import typing

from fastapi import APIRouter, Depends
from langgraph.graph.state import CompiledStateGraph

from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.infrastructure.telemetry.logger import get_logger
from app.interface_adapters.orchestrators.triage_graph_state import (
    TriageGraphState,
    map_state_to_triage_result,
)
from drivers.api.dependencies import get_triage_graph
from drivers.api.schemas.death_claim_request import DeathClaimRequest
from drivers.api.schemas.death_claim_response import DeathClaimResponse

router = APIRouter(tags=["triage"])
logger = get_logger(__name__)


@router.post("/triage", response_model=DeathClaimResponse)
def run_triage(
    req: DeathClaimRequest,
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
    triage_result = map_state_to_triage_result(result)

    return triage_result
