# Death Claim Triage: Phase 7 Implementation Plan (Live E2E Testing)

## Phase Summary

- **Scenario:** Death Claim Triage (Tree A)
- **Phase Goal:** Establish a suite of live, `@pytest.mark.live` decorated acceptance tests that execute the full end-to-end routing graph against the commercial OpenAI model, eliminating the need for manual UI/API clicking to prove correctness.
- **Status:** ready

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **PLAN_HUMAN_FINAL:** `.scratch/PLAN_HUMAN_FINAL.md` (Block 6 - Harden and Validate)
- **Tooling Validation Plan:** `plan/implementation/completed/tooling-validation-plan.md` (Live-Model Verification)

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- Defining new domain constraints or modifying the prompts (completed in Phase 5).
- UI automation testing via tools like Selenium or Playwright (tests will execute against the `TriageWorkflowFacade` directly or via `TestClient`).
- Mocked testing (this phase is strictly for live model execution).

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `tests/acceptance/features/test_live_e2e_triage.py` - The core E2E suite containing tests for all 3 canonical routing cases (Complete, Missing Info, Ambiguous).

### Modified Files

- `pytest.ini` - Register the `live` marker to ensure these tests can be optionally skipped in CI.
- `Makefile` - Add a `make test-live` command for explicitly invoking the `-m live` suite.

## Assertions & Behavior Contracts

- The tests MUST load the live `.env` variables (`LLM_MAIN_MODEL`, `LLM_MAIN_API_KEY`).
- The `test_live_e2e_triage.py` suite MUST be decorated with `@pytest.mark.live` and MUST be excluded from standard `make test` execution to protect developer billing metrics.
- The tests MUST assert the same structural outcomes as the mocked tests (e.g., correct `disposition`, generation of `case_summary` or `requirements_checklist`), proving the live prompts extract the expected structured data successfully.

## Deferred Items Touched (If Any)

| Deferred item | Current assumption used | Hardening still required |
|---------------|-------------------------|--------------------------|
| N/A           | N/A                     | N/A                      |

## Ordered Implementation Steps

Implement in this order:

1. Update `pytest.ini` to register the custom `live` marker.
2. Update the `Makefile` with a `test-live` target (`pytest -m live`).
3. Author `tests/acceptance/features/test_live_e2e_triage.py` leveraging the established `triage_workflow` fixture but configured with the live `LiveChatModelAdapter` instead of fakes.
4. Implement the 3 representative case assertions against the live endpoint.
5. Execute `make test-live` locally to verify the live execution succeeds and costs are negligible.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- Standard `make test` completes without hitting the OpenAI API.
- `make test-live` successfully hits the OpenAI API, returns successfully, and asserts the correct semantic structures were built for the 3 domain cases.

## Assumptions

- The developer executing `make test-live` has populated an `.env` or `.env.local` containing a valid, funded OpenAI API key.
