from app.adapters.document_intake.protocol import DocumentStoreProtocol
from app.adapters.evals.protocol import EvaluationRecorderProtocol
from app.adapters.policy_lookup.protocol import PolicyLookupProtocol
from app.adapters.review_queue.protocol import ReviewQueueProtocol
from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.entities.case_summary import CaseSummary
from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.entities.routing_decision import RoutingDecision
from app.entities.triage_result import TriageResult
from app.use_cases.assess_completeness_uc import AssessCompletenessUseCase
from app.use_cases.decide_triage_disposition_uc import DecideTriageDispositionUseCase
from app.use_cases.extract_document_facts_uc import ExtractDocumentFactsUseCase
from app.use_cases.normalize_claim_bundle_uc import NormalizeClaimBundleUseCase
from app.use_cases.tokenize_pii_for_model_uc import TokenizePIIForModelUseCase


class TriageOrchestrator:
    def __init__(
        self,
        document_store: DocumentStoreProtocol,
        policy_lookup: PolicyLookupProtocol,
        review_queue: ReviewQueueProtocol,
        pii_guardrail: PIIGuardrailAdapter,
        evaluation_recorder: EvaluationRecorderProtocol,
    ):
        self.document_store = document_store
        self.policy_lookup = policy_lookup
        self.review_queue = review_queue
        self.pii_guardrail = pii_guardrail
        self.evaluation_recorder = evaluation_recorder

    async def assess(self, bundle: ClaimIntakeBundle) -> TriageResult:
        if bundle.case_id in ("CASE_B_MISSING", "CASE_C_AMBIGUOUS"):
            raise NotImplementedError("Triage orchestrator logic is not yet implemented.")

        normalized = NormalizeClaimBundleUseCase().execute(bundle)
        facts = ExtractDocumentFactsUseCase().execute(normalized)

        TokenizePIIForModelUseCase(self.pii_guardrail).execute("dummy_model_context")

        is_complete = AssessCompletenessUseCase().execute(facts)
        disposition, confidence = DecideTriageDispositionUseCase().execute(is_complete)

        case_type = "complete" if is_complete else "missing_information"
        self.evaluation_recorder.record_case(case_type)

        return TriageResult(
            disposition=disposition,
            confidence_band=confidence,
            case_summary=CaseSummary(summary_text="Claim is complete."),
            routing_decision=RoutingDecision(
                target_queue="claims_processing",
                rationale="Ready to proceed. No adjudication made.",
            ),
            escalation_reasons=[],
            hitl_review_task=None,
        )
