import operator
from typing import Annotated, TypedDict

from app.entities.case_summary import CaseSummary
from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.entities.routing_decision import RoutingDecision
from app.entities.triage_result import TriageResult


class TriageGraphState(TypedDict, total=False):
    """
    Accumulated state for the Death Claim Triage workflow.
    Uses TypedDict with primitive types and data classes to allow predictable reduction.
    """

    # Input
    claim_bundle: ClaimIntakeBundle

    # Extracted data and logic routing properties
    document_facts: dict
    is_complete: bool
    is_ambiguous: bool

    # TriageResult fields
    disposition: str
    confidence_band: str
    case_summary: CaseSummary | None
    routing_decision: RoutingDecision | None
    requirements_checklist: str | None
    follow_up_message: str | None
    follow_up_message_quality_markers: Annotated[list[str], operator.add]
    hitl_review_task: str | None
    reviewability_flags: Annotated[list[str], operator.add]
    escalation_reasons: Annotated[list[str], operator.add]
    escalation_rationale: str | None


def map_state_to_triage_result(state: TriageGraphState) -> TriageResult:
    """Maps the accumulated LangGraph state to the final TriageResult entity."""
    return TriageResult(
        disposition=state.get("disposition", "unknown"),
        confidence_band=state.get("confidence_band", "unknown"),
        case_summary=state.get("case_summary"),
        routing_decision=state.get("routing_decision"),
        requirements_checklist=state.get("requirements_checklist"),
        follow_up_message=state.get("follow_up_message"),
        follow_up_message_quality_markers=state.get("follow_up_message_quality_markers", []),
        hitl_review_task=state.get("hitl_review_task"),
        reviewability_flags=state.get("reviewability_flags", []),
        escalation_reasons=state.get("escalation_reasons", []),
        escalation_rationale=state.get("escalation_rationale"),
    )
