from typing import Any

from app.adapters.model.protocol import ModelAdapter
from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.interface_adapters.orchestrators.nodes.generate_artifacts_node import generate_summary_artifact
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState


def build_generate_proceed_artifacts_node(model: ModelAdapter):
    def generate_proceed_artifacts_node(state: TriageGraphState) -> dict[str, Any]:
        disposition = state.get("disposition", "unknown")
        tokenized_facts = state.get("tokenized_document_facts", {})
        updates: dict[str, Any] = {}
        logger = get_logger(__name__).bind(node="generate_proceed_artifacts")
        op_log = logger.bind(operation="generate_proceed_artifacts")
        bundle = state.get("claim_bundle")
        if bundle is None:
            op_log.warning("validation_failed", reason="missing_claim_bundle")
            raise ValueError("claim_bundle is required in state to generate artifacts")
        log = op_log.bind(
            case_id=bundle.case_id,
            disposition=disposition,
        )
        log.info("started", fact_count=len(tokenized_facts))

        try:
            summary = generate_summary_artifact(model, tokenized_facts)
            if summary:
                updates["case_summary"] = summary

            log.info("completed", generated_fields=sorted(updates.keys()))
            return updates
        except Exception as e:
            log_exception(log, "failed", e)
            raise

    return generate_proceed_artifacts_node
