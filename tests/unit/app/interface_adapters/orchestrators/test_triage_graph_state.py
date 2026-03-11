from unittest.mock import MagicMock

from app.entities.case_summary import CaseSummary
from app.entities.routing_decision import RoutingDecision
from app.interface_adapters.orchestrators.triage_graph_state import (
    TriageGraphState,
    map_state_to_triage_result,
)


def test_map_state_to_triage_result_full_state():
    mock_bundle = MagicMock()

    state: TriageGraphState = {
        "claim_bundle": mock_bundle,
        "is_complete": True,
        "is_ambiguous": False,
        "disposition": "approved",
        "confidence_band": "high",
        "case_summary": CaseSummary(summary_text="Completed automatically"),
        "routing_decision": RoutingDecision(target_queue="auto_adjudication", rationale="All good"),
        "requirements_checklist": "- Need signature",
        "follow_up_message": "Please sign.",
        "follow_up_message_quality_markers": ["clear_instructions"],
        "hitl_review_task": "Review signature",
        "reviewability_flags": ["missing_signature"],
        "escalation_reasons": ["fraud_suspicion"],
        "escalation_rationale": "Looks phishy",
    }

    result = map_state_to_triage_result(state)

    assert result.disposition == "approved"
    assert result.confidence_band == "high"
    assert result.case_summary and result.case_summary.summary_text == "Completed automatically"
    assert result.routing_decision and result.routing_decision.target_queue == "auto_adjudication"
    assert result.requirements_checklist == "- Need signature"
    assert result.follow_up_message == "Please sign."
    assert result.follow_up_message_quality_markers == ["clear_instructions"]
    assert result.hitl_review_task == "Review signature"
    assert result.reviewability_flags == ["missing_signature"]
    assert result.escalation_reasons == ["fraud_suspicion"]
    assert result.escalation_rationale == "Looks phishy"


def test_map_state_to_triage_result_empty_state():
    mock_bundle = MagicMock()

    state: TriageGraphState = {
        "claim_bundle": mock_bundle,
        "is_complete": False,
        "is_ambiguous": False,
    }

    result = map_state_to_triage_result(state)

    assert result.disposition == "unknown"
    assert result.confidence_band == "unknown"
    assert result.case_summary is None
    assert result.routing_decision is None
    assert result.requirements_checklist is None
    assert result.follow_up_message is None
    assert result.follow_up_message_quality_markers == []
    assert result.hitl_review_task is None
    assert result.reviewability_flags == []
    assert result.escalation_reasons == []
    assert result.escalation_rationale is None
