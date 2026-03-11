import os

import dspy
import streamlit as st
from langgraph.graph.state import CompiledStateGraph

from app.adapters.document_intake.fake import FakeDocumentStore
from app.adapters.evals.fake import FakeEvaluationRecorder
from app.adapters.model.fake import FakeModelAdapter
from app.adapters.model.live_chat_model_adapter import LiveChatModelAdapter
from app.adapters.policy_lookup.fake import FakePolicyLookup
from app.adapters.review_queue.fake import FakeReviewQueue
from app.adapters.safety.fake import FakePIIGuardrail
from app.adapters.safety.vaultless_guardrail import VaultlessPIIGuardrail
from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.interface_adapters.orchestrators.triage_graph_factory import (
    AdapterRegistry,
    build_triage_graph,
)
from drivers.ui.config import UIConfig

logger = get_logger(__name__).bind(driver="StreamlitDependencies", surface="streamlit")


# Bumping to clear cache
@st.cache_resource
def get_triage_graph(config: UIConfig) -> CompiledStateGraph:
    """
    Builds the triage graph injecting live explicit adapters
    if env domain vars are set, otherwise falls back to fakes.
    Uses st.cache_resource to prevent recompiling the graph on every render.
    """
    log = logger.bind(operation="get_triage_graph")
    log.info("started")
    try:
        if config.llm_main_model and config.llm_main_api_key:
            model_adapter = LiveChatModelAdapter(
                model_name=config.llm_main_model,
                api_key=config.llm_main_api_key,
                api_base=config.llm_main_api_base,
                requests_per_minute=config.llm_main_requests_per_minute,
            )
            model_mode = "live"
        else:
            model_adapter = FakeModelAdapter()
            model_mode = "fake"

        if config.llm_guardrail_secret_key:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            model_path = os.path.join(base_dir, "app", "adapters", "safety", "compiled_pii_extractor.json")

            # Configure global DSPy LM if provided.
            if config.llm_guardrail_model:
                lm = dspy.LM(
                    config.llm_guardrail_model,
                    api_base=config.llm_guardrail_api_base or "http://localhost:11434",
                    api_key=config.llm_guardrail_api_key,
                )
                dspy.settings.configure(lm=lm)

            pii_guardrail = VaultlessPIIGuardrail(
                secret_key_hex=config.llm_guardrail_secret_key, compiled_model_path=model_path
            )
            pii_mode = "vaultless"
        else:
            pii_guardrail = FakePIIGuardrail()
            pii_mode = "fake"

        adapters = AdapterRegistry(
            document_store=FakeDocumentStore(),
            policy_lookup=FakePolicyLookup(),
            review_queue=FakeReviewQueue(),
            pii_guardrail=pii_guardrail,
            model=model_adapter,
            evaluation_recorder=FakeEvaluationRecorder(),
        )
        graph = build_triage_graph(adapters)
        log.info("completed", model_mode=model_mode, pii_mode=pii_mode)
        return graph
    except Exception as e:
        log_exception(log, "failed", e)
        raise
