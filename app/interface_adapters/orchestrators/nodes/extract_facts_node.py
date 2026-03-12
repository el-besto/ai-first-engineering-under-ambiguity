from typing import Any

from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.extract_document_facts_uc import ExtractDocumentFactsUseCase


def extract_facts_node(state: TriageGraphState) -> dict[str, Any]:
    """
    Node for extracting document facts.
    Wraps the ExtractDocumentFactsUseCase and updates the state.
    """
    logger = get_logger(__name__).bind(node="extract_facts")
    op_log = logger.bind(operation="extract_facts")
    bundle = state.get("claim_bundle")
    if isinstance(bundle, dict):
        from app.entities.claim_intake_bundle import ClaimIntakeBundle

        bundle = ClaimIntakeBundle(**bundle)

    if not bundle:
        op_log.warning("validation_failed", reason="missing_claim_bundle")
        raise ValueError("claim_bundle is required in state to extract facts")

    log = op_log.bind(case_id=bundle.case_id)
    log.info("started", document_count=len(bundle.documents))
    try:
        # Delegate extraction to the deterministic use case.
        use_case = ExtractDocumentFactsUseCase(log)
        facts = use_case.execute(bundle)
        log.info("completed", fact_count=len(facts))
        return {"document_facts": facts}
    except Exception as e:
        log_exception(log, "failed", e)
        raise
