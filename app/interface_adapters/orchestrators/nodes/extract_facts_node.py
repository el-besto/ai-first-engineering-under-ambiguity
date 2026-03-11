from typing import Any

from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.extract_document_facts_uc import ExtractDocumentFactsUseCase


def extract_facts_node(state: TriageGraphState) -> dict[str, Any]:
    """
    Node for extracting document facts.
    Wraps the ExtractDocumentFactsUseCase and updates the state.
    """
    bundle = state.get("claim_bundle")
    if not bundle:
        raise ValueError("claim_bundle is required in state to extract facts")

    use_case = ExtractDocumentFactsUseCase()
    facts = use_case.execute(bundle)
    return {"document_facts": facts}
