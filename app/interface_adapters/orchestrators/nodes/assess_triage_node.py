from typing import Any

from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.assess_completeness_uc import AssessCompletenessUseCase
from app.use_cases.decide_triage_disposition_uc import DecideTriageDispositionUseCase
from app.use_cases.detect_ambiguity_uc import DetectAmbiguityUseCase


def assess_triage_node(state: TriageGraphState) -> dict[str, Any]:
    """
    Node for assessing completeness, ambiguity and routing.
    Runs the deterministic checks and aggregates the results into state updates.
    """
    logger = get_logger(__name__).bind(node="assess_triage")
    op_log = logger.bind(operation="assess_triage")
    document_facts = state.get("document_facts", {})
    bundle = state.get("claim_bundle")
    if bundle is None:
        op_log.warning("validation_failed", reason="missing_claim_bundle")
        raise ValueError("claim_bundle is required in state to assess triage")

    log = op_log.bind(case_id=bundle.case_id)
    log.info("started", fact_count=len(document_facts))
    try:
        # 1. Assess completeness.
        is_complete = AssessCompletenessUseCase(log).execute(document_facts)

        # 2. Detect ambiguity.
        is_ambiguous = DetectAmbiguityUseCase(log).execute(document_facts)

        # 3. Decide disposition.
        disposition, confidence_band = DecideTriageDispositionUseCase(log).execute(
            is_complete=is_complete, is_ambiguous=is_ambiguous
        )

        updates: dict[str, Any] = {
            "is_complete": is_complete,
            "is_ambiguous": is_ambiguous,
            "disposition": disposition,
            "confidence_band": confidence_band,
        }

        log.info("completed", selected_disposition=disposition, confidence_band=confidence_band)
        return updates
    except Exception as e:
        log_exception(log, "failed", e)
        raise
