import pytest

from app.adapters.document_intake.fake import FakeDocumentStore
from app.adapters.evals.fake import FakeEvaluationRecorder
from app.adapters.policy_lookup.fake import FakePolicyLookup
from app.adapters.review_queue.fake import FakeReviewQueue
from app.adapters.safety.fake import FakePIIGuardrail
from app.interface_adapters.orchestrators.triage_workflow import TriageOrchestrator


@pytest.fixture
def fake_document_store():
    return FakeDocumentStore()


@pytest.fixture
def fake_policy_lookup():
    return FakePolicyLookup()


@pytest.fixture
def fake_review_queue():
    return FakeReviewQueue()


@pytest.fixture
def fake_pii_guardrail():
    return FakePIIGuardrail()


@pytest.fixture
def fake_evaluation_recorder():
    return FakeEvaluationRecorder()


@pytest.fixture
def triage_workflow(
    fake_document_store,
    fake_policy_lookup,
    fake_review_queue,
    fake_pii_guardrail,
    fake_evaluation_recorder,
):
    return TriageOrchestrator(
        document_store=fake_document_store,
        policy_lookup=fake_policy_lookup,
        review_queue=fake_review_queue,
        pii_guardrail=fake_pii_guardrail,
        evaluation_recorder=fake_evaluation_recorder,
    )
