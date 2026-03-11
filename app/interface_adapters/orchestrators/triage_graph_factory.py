from dataclasses import dataclass

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.adapters.document_intake.protocol import DocumentStoreProtocol
from app.adapters.evals.protocol import EvaluationRecorderProtocol
from app.adapters.policy_lookup.protocol import PolicyLookupProtocol
from app.adapters.review_queue.protocol import ReviewQueueProtocol
from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState


@dataclass(slots=True, frozen=True)
class AdapterRegistry:
    """Registry holding all required adapters for the triage graph."""

    document_store: DocumentStoreProtocol
    policy_lookup: PolicyLookupProtocol
    review_queue: ReviewQueueProtocol
    pii_guardrail: PIIGuardrailAdapter
    evaluation_recorder: EvaluationRecorderProtocol


def build_triage_graph(adapters: AdapterRegistry) -> CompiledStateGraph:
    """
    Factory function to build and compile the Triage StateGraph.
    Uses closure to inject the AdapterRegistry into nodes without polluting the graph state.
    """
    workflow = StateGraph(TriageGraphState)

    # Mock placeholder nodes that simply return the state untouched
    # In future phases, these will be replaced with actual use cases / logic

    def normalize_claim_bundle(state: TriageGraphState) -> dict:
        return {}

    def extract_document_facts(state: TriageGraphState) -> dict:
        return {}

    def assess_completeness(state: TriageGraphState) -> dict:
        return {}

    def detect_ambiguity(state: TriageGraphState) -> dict:
        return {}

    def decide_triage_disposition(state: TriageGraphState) -> dict:
        return {}

    def handle_request_more_information(state: TriageGraphState) -> dict:
        return {}

    def handle_escalate_to_human_review(state: TriageGraphState) -> dict:
        return {}

    # Define nodes
    workflow.add_node("normalize_claim_bundle", normalize_claim_bundle)
    workflow.add_node("extract_document_facts", extract_document_facts)
    workflow.add_node("assess_completeness", assess_completeness)
    workflow.add_node("detect_ambiguity", detect_ambiguity)
    workflow.add_node("decide_triage_disposition", decide_triage_disposition)
    workflow.add_node("handle_request_more_information", handle_request_more_information)
    workflow.add_node("handle_escalate_to_human_review", handle_escalate_to_human_review)

    # Basic linear flow for mock/placeholder purposes
    workflow.add_edge(START, "normalize_claim_bundle")
    workflow.add_edge("normalize_claim_bundle", "extract_document_facts")
    workflow.add_edge("extract_document_facts", "assess_completeness")
    workflow.add_edge("assess_completeness", "detect_ambiguity")
    workflow.add_edge("detect_ambiguity", "decide_triage_disposition")

    # For now, end at disposition. Branching logic comes in later phases.
    workflow.add_edge("decide_triage_disposition", END)

    return workflow.compile()
