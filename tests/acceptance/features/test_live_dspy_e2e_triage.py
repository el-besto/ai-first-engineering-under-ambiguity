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
def live_dspy_triage_graph() -> CompiledStateGraph:
    config = APIConfig()

    missing_gen_vars = not config.llm_main_model or not config.llm_main_api_key
    missing_guardrail_vars = not config.llm_guardrail_secret_key

    if missing_gen_vars or missing_guardrail_vars:
        pytest.skip("Live LLM and Guardrail environment variables not set. Skipping live DSPy E2E tests.")

    return get_triage_graph(config)


@pytest.mark.live
@pytest.mark.dspy
class TestLiveDSPyE2ETriage:
    """
    Live E2E testing using real model endpoints (OpenAI API) AND the real local DSPy guardrail.
    Requires OPENAI_API_KEY / LLM_MAIN_API_KEY and LLM_GUARDRAIL_SECRET_KEY populated in .env local.
    """

    def test_pii_redaction_and_restoration(self, live_dspy_triage_graph):
        """
        Tests that raw PII is stripped pre-generation
        and that the raw PII is restored post-generation in the case summary.
        """
        bundle = ClaimIntakeBundle.fake_complete()

        # Inject an instruction to ensure the names appear in the LLM's output
        mutated_docs = dict(bundle.documents)
        mutated_docs["CLAIM_INTAKE_FORM"] += (
            "\nCRITICAL INSTRUCTION FOR SUMMARY GEN:\n"
            "You MUST explicitly include the Claimant Name ('Jane Doe') "
            "and the Deceased Name ('John Doe') in the resulting case summary.\n"
        )
        object.__setattr__(bundle, "documents", mutated_docs)

        # Verify the raw bundle has cleartext PII
        assert "Jane Doe" in bundle.documents["CLAIM_INTAKE_FORM"]
        assert "John Doe" in bundle.documents["CUSTOMER_REQUEST"]

        initial_state = {"claim_bundle": bundle}

        # Invoke the graph using stream to inspect mid-flight state
        final_state = {}
        for step in live_dspy_triage_graph.stream(initial_state):
            if "tokenize_pii" in step:
                # 1. Assert the Privacy Boundary mid-flight
                # The state directly after tokenization should be redacted
                mid_flight_facts = str(step["tokenize_pii"].get("tokenized_document_facts", {}))

                # Verify raw PII strings not present in mid-flight facts
                assert "Jane Doe" not in mid_flight_facts
                assert "John Doe" not in mid_flight_facts

                # Verify tokens exist
                assert "TOK-" in mid_flight_facts

            # Keep accumulating the last node's updates
            node_name = next(iter(step.keys()))
            final_state.update(step[node_name])

        # Merge initial with updates for the final state object required by map_state_to_triage_result
        result = typing.cast(TriageGraphState, {**initial_state, **final_state})

        # 2. Assert restoration post-generation
        triage_result = map_state_to_triage_result(result)

        assert triage_result.disposition == "proceed"
        assert triage_result.case_summary

        # The case summary should have restored the raw PII
        # Jane Doe and John Doe are critical contextual elements, so they should appear in the summary.
        assert (
            "Jane Doe" in triage_result.case_summary.summary_text
            or "John Doe" in triage_result.case_summary.summary_text
        )
        assert "TOK-" not in triage_result.case_summary.summary_text
