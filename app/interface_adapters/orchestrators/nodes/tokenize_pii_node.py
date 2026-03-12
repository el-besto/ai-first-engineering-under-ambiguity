from typing import Any

from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.tokenize_pii_for_model_uc import TokenizePIIForModelUseCase


def build_tokenize_pii_node(pii_guardrail: PIIGuardrailAdapter):
    def tokenize_pii_node(state: TriageGraphState) -> dict[str, Any]:
        """
        Tokenizes PII in document_facts before passing to generative model nodes.
        Places tokenized output in 'tokenized_document_facts' to preserve the original
        'document_facts' for internal use.
        """
        logger = get_logger(__name__).bind(node="tokenize_pii")
        op_log = logger.bind(operation="tokenize_pii")
        bundle = state.get("claim_bundle")
        if bundle is None:
            op_log.warning("validation_failed", reason="missing_claim_bundle")
            raise ValueError("claim_bundle is required in state to tokenize PII")
        facts = state.get("document_facts", {})
        log = op_log.bind(case_id=bundle.case_id)
        if not facts:
            log.info("completed", tokenized=False)
            return {}

        log.info("started", fact_count=len(facts))
        try:
            # Serialize the entire facts payload into a JSON string to batch request the guardrail
            uc = TokenizePIIForModelUseCase(pii_guardrail, log)
            import json

            docs = facts.get("document_texts", {})
            facts_without_docs = {k: v for k, v in facts.items() if k != "document_texts"}

            payload_str = json.dumps(facts_without_docs)
            tokenized_payload_str, _ = uc.execute(payload_str)
            tokenized_facts = json.loads(tokenized_payload_str)

            tokenized_docs = {}
            for doc_name, text in docs.items():
                tok_text, _ = uc.execute(text)
                tokenized_docs[doc_name] = tok_text

            tokenized_facts["document_texts"] = tokenized_docs

            log.info("completed", tokenized=True)
            return {
                "tokenized_document_facts": tokenized_facts,
            }
        except Exception as e:
            log_exception(log, "failed", e)
            raise

    return tokenize_pii_node
