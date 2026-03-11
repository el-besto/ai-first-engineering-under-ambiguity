from typing import Any

from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.tokenize_pii_for_model_uc import TokenizePIIForModelUseCase


def build_tokenize_pii_node(pii_guardrail: PIIGuardrailAdapter):
    def tokenize_pii_node(state: TriageGraphState) -> dict[str, Any]:
        """
        Tokenizes PII in document_facts before passing to generative model nodes.
        Places tokenized output in 'document_facts' to replace sensitive data,
        or into a new field depending on state. For now, we update 'document_facts'
        with tokenized data to prevent leakage, but we should make sure we don't
        lose the original facts if needed elsewhere.
        """
        facts = state.get("document_facts", {})
        if not facts:
            return {}

        # We need to serialize facts to string, tokenize, and deserialize,
        # or recursively tokenize the dictionary. The use case takes `raw_text: str`.
        uc = TokenizePIIForModelUseCase(pii_guardrail)

        def recursive_tokenize(obj: Any) -> Any:
            if isinstance(obj, str):
                tokenized_text, _ = uc.execute(obj)
                return tokenized_text
            elif isinstance(obj, dict):
                return {k: recursive_tokenize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [recursive_tokenize(v) for v in obj]
            return obj

        tokenized_facts = recursive_tokenize(facts)

        return {
            "document_facts": tokenized_facts,
        }

    return tokenize_pii_node
