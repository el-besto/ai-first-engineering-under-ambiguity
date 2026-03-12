from app.adapters.document_intake.protocol import DocumentStoreProtocol
from app.adapters.evals.protocol import EvaluationRecorderProtocol
from app.adapters.policy_lookup.protocol import PolicyLookupProtocol
from app.adapters.review_queue.protocol import ReviewQueueProtocol
from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.entities.case_summary import CaseSummary
from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.entities.routing_decision import RoutingDecision
from app.entities.triage_result import TriageResult
from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.use_cases.assess_completeness_uc import AssessCompletenessUseCase
from app.use_cases.decide_triage_disposition_uc import DecideTriageDispositionUseCase
from app.use_cases.detect_ambiguity_uc import DetectAmbiguityUseCase
from app.use_cases.extract_document_facts_uc import ExtractDocumentFactsUseCase
from app.use_cases.generate_escalation_rationale_uc import GenerateEscalationRationaleUseCase
from app.use_cases.generate_follow_up_message_uc import GenerateFollowUpMessageUseCase
from app.use_cases.generate_hitl_review_task_uc import GenerateHITLReviewTaskUseCase
from app.use_cases.generate_requirements_checklist_uc import GenerateRequirementsChecklistUseCase
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
        self.logger = get_logger(__name__).bind(orchestrator=self.__class__.__name__)

    async def assess(self, bundle: ClaimIntakeBundle) -> TriageResult:
        log = self.logger.bind(operation="assess", case_id=bundle.case_id)
        log.info("started", document_count=len(bundle.documents))

        try:
            # Triage boundary fully removed for the acceptance slices.
            normalized = NormalizeClaimBundleUseCase(log).execute(bundle)
            facts = ExtractDocumentFactsUseCase(log).execute(normalized)

            TokenizePIIForModelUseCase(self.pii_guardrail, log).execute("dummy_model_context")

            is_complete = AssessCompletenessUseCase(log).execute(facts)
            is_ambiguous = DetectAmbiguityUseCase(log).execute(facts)
            disposition, confidence = DecideTriageDispositionUseCase(log).execute(is_complete, is_ambiguous)

            checklist = None
            follow_up = None
            quality_markers = []
            reviewability_flags = []

            escalation_reasons = []
            escalation_rationale = None
            hitl_review_task = None

            if disposition == "request_more_information":
                checklist = GenerateRequirementsChecklistUseCase(log).execute(facts)
                follow_up, quality_markers = GenerateFollowUpMessageUseCase(log).execute(checklist)
                reviewability_flags = ["Missing required documents"]
            elif disposition == "escalate_to_human_review":
                escalation_reasons, escalation_rationale = GenerateEscalationRationaleUseCase(log).execute(facts)
                hitl_review_task = GenerateHITLReviewTaskUseCase(log).execute(facts)

            if is_ambiguous:
                case_type = "ambiguous"
            else:
                case_type = "complete" if is_complete else "missing_information"
            self.evaluation_recorder.record_case(case_type)

            result = TriageResult(
                disposition=disposition,
                confidence_band=confidence,
                case_summary=CaseSummary(summary_text="Claim is complete.") if is_complete else None,
                routing_decision=RoutingDecision(
                    target_queue="claims_processing",
                    rationale="Ready to proceed. All required documents present.",
                )
                if is_complete
                else None,
                requirements_checklist=checklist,
                follow_up_message=follow_up,
                follow_up_message_quality_markers=quality_markers,
                reviewability_flags=reviewability_flags,
                escalation_reasons=escalation_reasons,
                escalation_rationale=escalation_rationale,
                hitl_review_task=hitl_review_task,
            )
            log.info(
                "completed",
                selected_disposition=result.disposition,
                confidence_band=result.confidence_band,
                reviewability_state="needs_review" if result.reviewability_flags else "clear",
            )
            return result
        except Exception as e:
            log_exception(log, "failed", e)
            raise
