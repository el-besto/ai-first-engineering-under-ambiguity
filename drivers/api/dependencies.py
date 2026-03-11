from fastapi import Depends
from langgraph.graph.state import CompiledStateGraph

from app.adapters.document_intake.fake import FakeDocumentStore
from app.adapters.evals.fake import FakeEvaluationRecorder
from app.adapters.model.fake import FakeModelAdapter
from app.adapters.model.live_chat_model_adapter import LiveChatModelAdapter
from app.adapters.policy_lookup.fake import FakePolicyLookup
from app.adapters.review_queue.fake import FakeReviewQueue
from app.adapters.safety.fake import FakePIIGuardrail
from app.interface_adapters.orchestrators.triage_graph_factory import (
    AdapterRegistry,
    build_triage_graph,
)
from drivers.api.config import APIConfig


def get_api_config() -> APIConfig:
    return APIConfig()


def get_triage_graph(config: APIConfig = Depends(get_api_config)) -> CompiledStateGraph:  # noqa: B008
    """
    Builds the triage graph injecting live explicit adapters
    if env domain vars are set, otherwise falls back to fakes.
    """
    if config.llm_main_model and config.llm_main_api_key:
        model_adapter = LiveChatModelAdapter(
            model_name=config.llm_main_model,
            api_key=config.llm_main_api_key,
            api_base=config.llm_main_api_base,
            requests_per_minute=config.llm_main_requests_per_minute,
        )
    else:
        model_adapter = FakeModelAdapter()

    adapters = AdapterRegistry(
        document_store=FakeDocumentStore(),
        policy_lookup=FakePolicyLookup(),
        review_queue=FakeReviewQueue(),
        pii_guardrail=FakePIIGuardrail(),
        model=model_adapter,
        evaluation_recorder=FakeEvaluationRecorder(),
    )
    return build_triage_graph(adapters)
