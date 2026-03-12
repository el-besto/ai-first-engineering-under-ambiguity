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


@router.post(
    "/triage",
    response_model=DeathClaimResponse,
    summary="Run Death Claim Triage",
    description=(
        "Executes the automated triage workflow for a death claim.\n\n"
        "**Demo / Testing Fakes:**\n"
        "To easily test the different LangGraph pathways in the PoC without uploading real documents, "
        "you can pass the following canonical values for `policy_number`:\n"
        "- `A` or `COMPLETE` -> Complete claim scenario\n"
        "- `B` or `MISSING` -> Missing information scenario (Missing claimant signature, date of death, etc.)\n"
        "- `C` or `AMBIGUOUS` -> Ambiguous claim scenario (Inconsistent date of death)\n"
    ),
)
def run_triage(
    req: DeathClaimRequest,
    graph: CompiledStateGraph = Depends(get_triage_graph),  # noqa: B008
):
    # Map strict scenario names to bundle fakes for the PoC.
    policy_str = req.policy_number.upper().strip()
    if policy_str == "A" or "COMPLETE" in policy_str:
        bundle = ClaimIntakeBundle.fake_complete()
    elif policy_str == "B" or "MISSING" in policy_str:
        bundle = ClaimIntakeBundle.fake_missing_information()
    elif policy_str == "C" or "AMBIGUOUS" in policy_str:
        bundle = ClaimIntakeBundle.fake_ambiguous()
    else:
        # Default fallback is complete
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
