import pytest
from fastapi.testclient import TestClient

from drivers.api.config import APIConfig
from drivers.api.dependencies import get_api_config
from drivers.api.main import app


def get_test_api_config() -> APIConfig:
    return APIConfig(llm_main_api_key=None, llm_main_model=None, llm_guardrail_secret_key=None)


app.dependency_overrides[get_api_config] = get_test_api_config

client = TestClient(app)


@pytest.mark.feature("live_model_api_wiring")
def test_api_triage_complete_case():
    response = client.post("/triage", json={"policy_number": "CASE_A_COMPLETE"})
    assert response.status_code == 200
    data = response.json()

    assert data["disposition"] == "proceed"
    # Note: case_summary may be partial depending on Fake vs Live model
    assert data["case_summary"] is not None


@pytest.mark.feature("live_model_api_wiring")
def test_api_triage_missing_case():
    response = client.post("/triage", json={"policy_number": "CASE_B_MISSING"})
    assert response.status_code == 200
    data = response.json()

    assert data["disposition"] == "request_more_information"
    assert data["requirements_checklist"] is not None
    assert data["follow_up_message"] is not None


@pytest.mark.feature("live_model_api_wiring")
def test_api_triage_ambiguous_case():
    response = client.post("/triage", json={"policy_number": "CASE_C_AMBIGUOUS"})
    assert response.status_code == 200
    data = response.json()

    assert data["disposition"] == "escalate_to_human_review"
    assert data["hitl_review_task"] is not None
    assert data["escalation_reasons"]
