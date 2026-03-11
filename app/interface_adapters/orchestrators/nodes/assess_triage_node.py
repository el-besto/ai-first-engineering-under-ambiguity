from typing import Any

from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.assess_completeness_uc import AssessCompletenessUseCase
from app.use_cases.decide_triage_disposition_uc import DecideTriageDispositionUseCase
from app.use_cases.detect_ambiguity_uc import DetectAmbiguityUseCase
from app.use_cases.generate_escalation_rationale_uc import GenerateEscalationRationaleUseCase
from app.use_cases.generate_follow_up_message_uc import GenerateFollowUpMessageUseCase
from app.use_cases.generate_hitl_review_task_uc import GenerateHITLReviewTaskUseCase
from app.use_cases.generate_requirements_checklist_uc import (
    GenerateRequirementsChecklistUseCase,
)


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

    # 4. Generate Reviewability / Follow-up based on disposition
    if disposition == "request_more_information":
        checklist = GenerateRequirementsChecklistUseCase().execute(document_facts)
        msg, quality_markers = GenerateFollowUpMessageUseCase().execute(checklist)
        updates["requirements_checklist"] = checklist
        updates["follow_up_message"] = msg
        updates["follow_up_message_quality_markers"] = quality_markers

    elif disposition == "escalate_to_human_review":
        task = GenerateHITLReviewTaskUseCase().execute(document_facts)
        reasons, rationale = GenerateEscalationRationaleUseCase().execute(document_facts)
        updates["hitl_review_task"] = task
        updates["escalation_reasons"] = reasons
        updates["escalation_rationale"] = rationale

    return updates
