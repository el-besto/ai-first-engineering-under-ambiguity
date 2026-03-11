from langgraph.graph.state import CompiledStateGraph

from app.adapters.document_intake.fake import FakeDocumentStore
from app.adapters.evals.fake import FakeEvaluationRecorder
from app.adapters.policy_lookup.fake import FakePolicyLookup
from app.adapters.review_queue.fake import FakeReviewQueue
from app.adapters.safety.fake import FakePIIGuardrail
from app.interface_adapters.orchestrators.triage_graph_factory import (
    AdapterRegistry,
    build_triage_graph,
)


def test_build_triage_graph_compiles_successfully():
    adapters = AdapterRegistry(
        document_store=FakeDocumentStore(),
        policy_lookup=FakePolicyLookup(),
        review_queue=FakeReviewQueue(),
        pii_guardrail=FakePIIGuardrail(),
        evaluation_recorder=FakeEvaluationRecorder(),
    )

    graph = build_triage_graph(adapters)

    assert isinstance(graph, CompiledStateGraph)

    # Verify expected nodes were added
    expected_nodes = [
        "normalize_claim_bundle",
        "extract_document_facts",
        "assess_completeness",
        "detect_ambiguity",
        "decide_triage_disposition",
    ]

    for node in expected_nodes:
        assert node in graph.nodes
