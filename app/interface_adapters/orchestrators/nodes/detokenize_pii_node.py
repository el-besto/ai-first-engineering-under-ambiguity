from typing import Any

from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.entities.case_summary import CaseSummary
from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState


def build_detokenize_pii_node(pii_guardrail: PIIGuardrailAdapter):
    def recursive_detokenize(obj: Any) -> Any:
        if isinstance(obj, str):
            return pii_guardrail.detokenize(obj, {})
        elif isinstance(obj, dict):
            return {k: recursive_detokenize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [recursive_detokenize(v) for v in obj]
        elif isinstance(obj, CaseSummary):
            return CaseSummary(summary_text=pii_guardrail.detokenize(obj.summary_text, {}))
        return obj

    def detokenize_pii_node(state: TriageGraphState) -> dict[str, Any]:
        """
        Detokenizes all string fields in the state that may contain tokens.
        """
        updates: dict[str, Any] = {}
        logger = get_logger(__name__).bind(node="detokenize_pii")
        op_log = logger.bind(operation="detokenize_pii")
        bundle = state.get("claim_bundle")
        if bundle is None:
            op_log.warning("validation_failed", reason="missing_claim_bundle")
            raise ValueError("claim_bundle is required in state to detokenize PII")
        log = op_log.bind(case_id=bundle.case_id)
        log.info("started")

        try:
            # Detokenize only the state fields that may contain model-visible tokens.
            if "document_facts" in state:
                updates["document_facts"] = recursive_detokenize(state["document_facts"])

            if case_summary := state.get("case_summary"):
                updates["case_summary"] = recursive_detokenize(case_summary)

            if requirements_checklist := state.get("requirements_checklist"):
                updates["requirements_checklist"] = recursive_detokenize(requirements_checklist)

            if follow_up_message := state.get("follow_up_message"):
                updates["follow_up_message"] = recursive_detokenize(follow_up_message)

            if hitl_review_task := state.get("hitl_review_task"):
                updates["hitl_review_task"] = recursive_detokenize(hitl_review_task)

            if escalation_rationale := state.get("escalation_rationale"):
                updates["escalation_rationale"] = recursive_detokenize(escalation_rationale)

            if escalation_reasons := state.get("escalation_reasons"):
                updates["escalation_reasons"] = recursive_detokenize(escalation_reasons)

            log.info("completed", updated_fields=sorted(updates.keys()))
            return updates
        except Exception as e:
            log_exception(log, "failed", e)
            raise

    return detokenize_pii_node
