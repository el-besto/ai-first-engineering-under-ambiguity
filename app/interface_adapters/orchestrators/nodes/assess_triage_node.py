from typing import Any

from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.assess_completeness_uc import AssessCompletenessUseCase
from app.use_cases.decide_triage_disposition_uc import DecideTriageDispositionUseCase
from app.use_cases.detect_ambiguity_uc import DetectAmbiguityUseCase


def assess_triage_node(state: TriageGraphState) -> dict[str, Any]:
    """
    Node for assessing completeness, ambiguity and routing.
    Runs the deterministic checks and aggregates the results into state updates.
    """
    document_facts = state.get("document_facts", {})

    # 1. Assess Completeness
    is_complete = AssessCompletenessUseCase().execute(document_facts)

    # 2. Detect Ambiguity
    is_ambiguous = DetectAmbiguityUseCase().execute(document_facts)

    # 3. Decide Disposition
    disposition, confidence_band = DecideTriageDispositionUseCase().execute(
        is_complete=is_complete, is_ambiguous=is_ambiguous
    )

    updates: dict[str, Any] = {
        "is_complete": is_complete,
        "is_ambiguous": is_ambiguous,
        "disposition": disposition,
        "confidence_band": confidence_band,
    }

    return updates
