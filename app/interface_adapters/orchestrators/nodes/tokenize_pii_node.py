import json
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

        # Convert facts to string to tokenize them.
        facts_str = json.dumps(facts)
        tokenized_text, _ = uc.execute(facts_str)

        # Update state with the tokenized facts so that subsequent nodes (generate_artifacts)
        # do not see raw PII.
        # We replace document_facts with the tokenized version.
        # Alternatively, we could store it as 'tokenized_facts', but replacing it
        # strictly enforces the privacy boundary.
        tokenized_facts = json.loads(tokenized_text)

        return {
            "document_facts": tokenized_facts,
            # We don't store token_map back into the graph state implicitly,
            # we just ensure document_facts is now safe.
            # But wait, if we need it to detokenize? For now, we just pass tokenized text.
        }

    return tokenize_pii_node
