from app.adapters.document_intake.fake import FakeDocumentStore
from app.adapters.evals.fake import FakeEvaluationRecorder
from app.adapters.model.fake import FakeModelAdapter
from app.adapters.policy_lookup.fake import FakePolicyLookup
from app.adapters.review_queue.fake import FakeReviewQueue
from app.adapters.safety.fake import FakePIIGuardrail
from app.interface_adapters.orchestrators.triage_graph_factory import (
    AdapterRegistry,
    build_triage_graph,
)

adapters = AdapterRegistry(
    document_store=FakeDocumentStore(),
    policy_lookup=FakePolicyLookup(),
    review_queue=FakeReviewQueue(),
    pii_guardrail=FakePIIGuardrail(),
    model=FakeModelAdapter(),
    evaluation_recorder=FakeEvaluationRecorder(),
)

graph = build_triage_graph(adapters)
