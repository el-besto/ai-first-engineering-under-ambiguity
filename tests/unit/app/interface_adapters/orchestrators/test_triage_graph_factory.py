from langgraph.graph.state import CompiledStateGraph

from app.adapters.document_intake.fake import FakeDocumentStore
from app.adapters.evals.fake import FakeEvaluationRecorder
from app.adapters.policy_lookup.fake import FakePolicyLookup
from app.adapters.review_queue.fake import FakeReviewQueue
from app.adapters.safety.fake import FakePIIGuardrail
from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.interface_adapters.orchestrators.triage_graph_factory import (
    AdapterRegistry,
    build_triage_graph,
)


def _get_adapters():
    return AdapterRegistry(
        document_store=FakeDocumentStore(),
        policy_lookup=FakePolicyLookup(),
        review_queue=FakeReviewQueue(),
        pii_guardrail=FakePIIGuardrail(),
        evaluation_recorder=FakeEvaluationRecorder(),
    )


def test_build_triage_graph_compiles_successfully():
    graph = build_triage_graph(_get_adapters())

    assert isinstance(graph, CompiledStateGraph)

    # Verify expected nodes were added
    expected_nodes = [
        "extract_facts",
        "assess_triage",
    ]

    for node in expected_nodes:
        assert node in graph.nodes


def test_triage_graph_proceeds_for_complete_claim():
    graph = build_triage_graph(_get_adapters())

    bundle = ClaimIntakeBundle.fake_complete()
    initial_state = {"claim_bundle": bundle}

    final_state = graph.invoke(initial_state)

    assert final_state["is_complete"] is True
    assert final_state["is_ambiguous"] is False
    assert final_state["disposition"] == "proceed"
    assert final_state["confidence_band"] == "High"


def test_triage_graph_requests_info_for_missing_information():
    graph = build_triage_graph(_get_adapters())

    bundle = ClaimIntakeBundle.fake_missing_information()
    initial_state = {"claim_bundle": bundle}

    final_state = graph.invoke(initial_state)

    assert final_state["is_complete"] is False
    assert final_state["is_ambiguous"] is False
    assert final_state["disposition"] == "request_more_information"
    assert "requirements_checklist" in final_state
    assert "follow_up_message" in final_state
    assert final_state["requirements_checklist"]


def test_triage_graph_escalates_for_ambiguous_claim():
    graph = build_triage_graph(_get_adapters())

    bundle = ClaimIntakeBundle.fake_ambiguous()
    initial_state = {"claim_bundle": bundle}

    final_state = graph.invoke(initial_state)

    assert final_state["is_ambiguous"] is True
    assert final_state["disposition"] == "escalate_to_human_review"
    assert "hitl_review_task" in final_state
    assert "escalation_reasons" in final_state
    assert final_state["escalation_reasons"]
