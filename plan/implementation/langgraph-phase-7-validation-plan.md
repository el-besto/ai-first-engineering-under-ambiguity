# Death Claim Triage: Tooling Validation Plan (LangGraph Phase 7)

## Summary

Use this document for the local validation posture around LangGraph Phase 7: Live E2E Testing for the Death Claim Triage scenario.

This document specifically owns validation checks ensuring the completed graph accurately interacts with a live commercial model (OpenAI) to generate the expected triage outcomes without requiring manual UI/API manipulation.

## Current Source Inputs

- Root tracker: `plan/death-claim/workshop-spec.md`
- Phase tracker: `plan/implementation/completed/langgraph-phase-7-live-e2e-tests.md`
- Target slice: `tests/acceptance/features/test_live_e2e_triage.py`

## Validation Scope

Validate the expanded thin slice with checks for:

- **Live E2E Testing (Phase 7):** The automated test suite correctly boots the `LiveChatModelAdapter`, invokes the `TriageGraph`, issues requests to the OpenAI endpoint, and asserts structurally sound responses for all 3 canonical cases.

## Local Runtime Checks

Run the following local validations:

- Run `make test` locally to ensure standard deterministic mocked tests run without issuing external API calls.
- Inspect `tests/acceptance/features/test_live_e2e_triage.py` to ensure it is correctly decorated with `@pytest.mark.live`.

## Live-Model Validation

- Supply live credentials (`LLM_MAIN_API_KEY`, `LLM_MAIN_MODEL`) in your local `.env`.
- Execute `make test-live` to run the active suite.
- Ensure the OpenAI model returns proper format matching `case_summary` or `requirements_checklist_prompt` depending on the representative case context provided.

## Ordered Validation Steps

1. Verify `pytest.ini` properly registers the `live` marker.
2. Verify the `Makefile` contains a protected `test-live` command so standard CI runs dodge billing.
3. Run the live E2E tests for the 3 cases locally and inspect the API cost/telemetry.
4. Confirm successful structured output returns that satisfy the standard triage assertions.

## Validation Done Criteria

Validation is complete when:

- Mocked `make test` suites avoid any network calls completely.
- `make test-live` executes smoothly over the network.
- The behavior of the true LLM natively satisfies our core assertions on domain edge cases.

## Out Of Scope

- Validating UI or REST API surfaces dynamically.
- Performance scaling and parallelizing multiple OpenAI queries under load.
- Testing the local DSPy guardrail SLM (which is reserved for DSPy Phase 3 validation).

## Verification

Verify the validation pass with evidence that:

- `make test-live` output completes with passed assertions.

## Completion Report

Report the following at the end of a validation pass:

- The results and observed latency of the `make test-live` run.
- Telemetry/usage statistics associated with the test run.
- Any flakiness observed in real LLM generation outputs that caused test assertions to sporadically fail.

## Assumptions

- The developer executing the test has sufficient credentials / token allowance for standard execution.
