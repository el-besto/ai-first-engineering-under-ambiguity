import typing

from fastapi import APIRouter, Depends
from langgraph.graph.state import CompiledStateGraph

from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.interface_adapters.orchestrators.triage_graph_state import (
    TriageGraphState,
    map_state_to_triage_result,
)
from drivers.api.dependencies import get_triage_graph
from drivers.api.schemas.death_claim_request import DeathClaimRequest
from drivers.api.schemas.death_claim_response import DeathClaimResponse

router = APIRouter(tags=["triage"])
logger = get_logger(__name__).bind(route="/triage", surface="api")


@router.post("/triage", response_model=DeathClaimResponse)
def run_triage(
    req: DeathClaimRequest,
    graph: CompiledStateGraph = Depends(get_triage_graph),  # noqa: B008
):
    # Map strict scenario names to bundle fakes for the PoC.
    policy_str = req.policy_number.upper()
    if "MISSING" in policy_str:
        bundle = ClaimIntakeBundle.fake_missing_information()
    elif "AMBIGUOUS" in policy_str:
        bundle = ClaimIntakeBundle.fake_ambiguous()
    else:
        bundle = ClaimIntakeBundle.fake_complete()

    log = logger.bind(operation="run_triage", case_id=bundle.case_id)
    log.info("started")

    initial_state = {"claim_bundle": bundle}
    try:
        # Execute the graph.
        result = typing.cast(TriageGraphState, graph.invoke(initial_state))
        triage_result = map_state_to_triage_result(result)
        log.info(
            "completed",
            selected_disposition=triage_result.disposition,
            confidence_band=triage_result.confidence_band,
            reviewability_state="needs_review" if triage_result.reviewability_flags else "clear",
        )
        return triage_result
    except Exception as e:
        log_exception(log, "failed", e)
        raise
