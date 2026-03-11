import typing

import pytest
from langgraph.graph.state import CompiledStateGraph

from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.interface_adapters.orchestrators.triage_graph_state import (
    TriageGraphState,
    map_state_to_triage_result,
)
from drivers.api.config import APIConfig
from drivers.api.dependencies import get_triage_graph


@pytest.fixture
def live_triage_graph() -> CompiledStateGraph:
    config = APIConfig()
    if not config.llm_main_model or not config.llm_main_api_key:
        pytest.skip("Live LLM environment variables not set. Skipping live tests.")

    return get_triage_graph(config)


@pytest.mark.live
@pytest.mark.feature("live_e2e_triage")
class TestLiveE2ETriage:
    """
    Live E2E testing using real model endpoints.
    Requires OPENAI_API_KEY / LLM_MAIN_API_KEY populated in .env local.
    """

    def test_live_complete_case(self, live_triage_graph):
        bundle = ClaimIntakeBundle.fake_complete()
        initial_state = {"claim_bundle": bundle}
        result = typing.cast(TriageGraphState, live_triage_graph.invoke(initial_state))
        triage_result = map_state_to_triage_result(result)

        assert triage_result.disposition == "proceed"
        assert triage_result.confidence_band in ["High", "Medium"]
        assert triage_result.case_summary
        assert not triage_result.escalation_reasons
        assert not triage_result.hitl_review_task

    def test_live_missing_info_case(self, live_triage_graph):
        bundle = ClaimIntakeBundle.fake_missing_information()
        initial_state = {"claim_bundle": bundle}
        result = typing.cast(TriageGraphState, live_triage_graph.invoke(initial_state))
        triage_result = map_state_to_triage_result(result)

        assert triage_result.disposition == "request_more_information"
        assert triage_result.confidence_band in ["High", "Medium"]
        assert triage_result.requirements_checklist
        assert triage_result.follow_up_message
        assert triage_result.escalation_reasons == []
        assert "empathetic" in triage_result.follow_up_message_quality_markers

    def test_live_ambiguous_case(self, live_triage_graph):
        bundle = ClaimIntakeBundle.fake_ambiguous()
        initial_state = {"claim_bundle": bundle}
        result = typing.cast(TriageGraphState, live_triage_graph.invoke(initial_state))
        triage_result = map_state_to_triage_result(result)

        assert triage_result.disposition == "escalate_to_human_review"
        assert triage_result.confidence_band in ["Low", "Medium"]
        assert triage_result.hitl_review_task
        assert triage_result.escalation_reasons
        assert triage_result.escalation_rationale

    def test_live_api_triage_endpoint(self):
        """
        Validates the /triage FastAPI endpoint end-to-end with the live model.
        We do not mock `get_api_config` here so it uses the real environment.
        """
        from fastapi.testclient import TestClient

        from drivers.api.main import app

        config = APIConfig()
        if not config.llm_main_model or not config.llm_main_api_key:
            pytest.skip("Live LLM environment variables not set. Skipping API live test.")

        client = TestClient(app)

        response = client.post("/triage", json={"policy_number": "CASE_A_COMPLETE"})
        assert response.status_code == 200
        data = response.json()

        assert data["disposition"] == "proceed"
        assert data["confidence_band"] in ["High", "Medium"]
        assert data["case_summary"] is not None
        assert not data["escalation_reasons"]
        assert not data["hitl_review_task"]
