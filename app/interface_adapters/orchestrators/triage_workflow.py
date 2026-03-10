from app.adapters.document_intake.protocol import DocumentStoreProtocol
from app.adapters.evals.protocol import EvaluationRecorderProtocol
from app.adapters.policy_lookup.protocol import PolicyLookupProtocol
from app.adapters.review_queue.protocol import ReviewQueueProtocol
from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.entities.claim_intake_bundle import ClaimIntakeBundle


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

    def assess(self, bundle: ClaimIntakeBundle) -> dict:
        raise NotImplementedError("Triage orchestrator logic is not yet implemented.")
