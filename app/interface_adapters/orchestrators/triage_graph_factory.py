from dataclasses import dataclass

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.adapters.document_intake.protocol import DocumentStoreProtocol
from app.adapters.evals.protocol import EvaluationRecorderProtocol
from app.adapters.model.protocol import ModelAdapter
from app.adapters.policy_lookup.protocol import PolicyLookupProtocol
from app.adapters.review_queue.protocol import ReviewQueueProtocol
from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.interface_adapters.orchestrators.nodes.assess_triage_node import (
    assess_triage_node,
)
from app.interface_adapters.orchestrators.nodes.detokenize_pii_node import (
    build_detokenize_pii_node,
)
from app.interface_adapters.orchestrators.nodes.extract_facts_node import (
    extract_facts_node,
)
from app.interface_adapters.orchestrators.nodes.generate_hitl_artifacts_node import (
    build_generate_hitl_artifacts_node,
)
from app.interface_adapters.orchestrators.nodes.generate_missing_info_artifacts_node import (
    build_generate_missing_info_artifacts_node,
)
from app.interface_adapters.orchestrators.nodes.generate_proceed_artifacts_node import (
    build_generate_proceed_artifacts_node,
)
from app.interface_adapters.orchestrators.nodes.tokenize_pii_node import (
    build_tokenize_pii_node,
)
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState


@dataclass(slots=True, frozen=True)
class AdapterRegistry:
    """Registry holding all required adapters for the triage graph."""

    document_store: DocumentStoreProtocol
    policy_lookup: PolicyLookupProtocol
    review_queue: ReviewQueueProtocol
    pii_guardrail: PIIGuardrailAdapter
    model: ModelAdapter
    evaluation_recorder: EvaluationRecorderProtocol


def build_triage_graph(adapters: AdapterRegistry) -> CompiledStateGraph:
    """
    Factory function to build and compile the Triage StateGraph.
    Uses closure to inject the AdapterRegistry into nodes without polluting the graph state.
    """
    workflow = StateGraph(TriageGraphState)

    # Define nodes
    workflow.add_node("extract_facts", extract_facts_node)
    workflow.add_node("assess_triage", assess_triage_node)
    workflow.add_node("tokenize_pii", build_tokenize_pii_node(adapters.pii_guardrail))
    workflow.add_node("generate_proceed_artifacts", build_generate_proceed_artifacts_node(adapters.model))
    workflow.add_node("generate_missing_info_artifacts", build_generate_missing_info_artifacts_node(adapters.model))
    workflow.add_node("generate_hitl_artifacts", build_generate_hitl_artifacts_node(adapters.model))
    workflow.add_node("detokenize_pii", build_detokenize_pii_node(adapters.pii_guardrail))

    # Basic linear flow for Phase 2
    workflow.add_edge(START, "extract_facts")
    workflow.add_edge("extract_facts", "assess_triage")

    # Conditional routing based on disposition
    def route_disposition(state: TriageGraphState) -> str:
        return state.get("disposition", "unknown")

    workflow.add_conditional_edges(
        "assess_triage",
        route_disposition,
        {
            "proceed": "tokenize_pii",
            "request_more_information": "tokenize_pii",
            "escalate_to_human_review": "tokenize_pii",
        },
    )

    workflow.add_conditional_edges(
        "tokenize_pii",
        route_disposition,
        {
            "proceed": "generate_proceed_artifacts",
            "request_more_information": "generate_missing_info_artifacts",
            "escalate_to_human_review": "generate_hitl_artifacts",
        },
    )

    workflow.add_edge("generate_proceed_artifacts", "detokenize_pii")
    workflow.add_edge("generate_missing_info_artifacts", "detokenize_pii")
    workflow.add_edge("generate_hitl_artifacts", "detokenize_pii")
    workflow.add_edge("detokenize_pii", END)

    return workflow.compile()
