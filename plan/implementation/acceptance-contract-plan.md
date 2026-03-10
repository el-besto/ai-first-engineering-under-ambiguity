# Death-Claim: Acceptance Contract Plan

## Summary

Use the current death-claim scenario/design docs as the primary contract and implement the first real runnable acceptance test as a **framework-agnostic workflow-facade test** backed by **filesystem fixture bundles**.

Do not trim `plan/death-claim/tree-a-code-map.md` first. It is sufficient as the naming and boundary map. The acceptance test should only require a thin subset of that tree, not the whole proposed structure.

Chosen defaults:

- test target: `triage_workflow.assess(bundle)` style workflow facade
- fixture style: `tests/acceptance/fixtures/death_claim/...` directories
- LangGraph stays behind the acceptance boundary
- the first runnable test weakens assertions tied to deferred claimant-tone specifics

## Current Source Inputs

- Workshop spec: `plan/death-claim/workshop-spec.md`
- Deferred hardening: `plan/death-claim/deferred-hardening.md`
- Tree A code map: `plan/death-claim/tree-a-code-map.md`
- Tree A worked example: `plan/death-claim/tree-a-worked-example.md`
- Slice anchor: `plan/death-claim/steel-thread.md`

## Acceptance-Contract Files To Create

- `tests/acceptance/features/test_death_claim_intake_triage.py`
- `tests/acceptance/fixtures/death_claim/case_a_complete/`
- `tests/acceptance/fixtures/death_claim/case_b_missing_information/`
- `tests/acceptance/fixtures/death_claim/case_c_ambiguous/`
- `tests/acceptance/conftest.py`

The acceptance test should be derived from the workshop-spec sketch, not invented from the code map.

## Top-Level Test Boundary

The runnable acceptance test should target:

- `await triage_workflow.assess(claim_bundle)`

The acceptance boundary should hide whether the implementation is:

- a direct orchestrator call
- a LangGraph-backed workflow
- a thin service object over Tree A use cases

## Minimal Supporting Production Surface

Only the minimum supporting surface required to satisfy the acceptance contract should exist:

- input/result objects for:
  - `ClaimIntakeBundle`
  - `TriageResult`
  - completeness / ambiguity / reviewability outputs
- a workflow owner that can:
  - normalize bundle
  - assemble context
  - tokenize PII
  - assess completeness
  - detect ambiguity
  - assess reviewability
  - choose disposition
  - generate disposition-specific artifacts
- fake collaborators for:
  - policy lookup
  - document store / intake
  - review queue
  - PII guardrail
  - evaluation recorder

The full Tree A tree does not need to exist before the test is written. Only the pieces required to satisfy the acceptance contract need to exist.

## Assertions To Keep

- complete case:
  - `disposition == "proceed"`
  - `confidence_band == "High"`
  - `case_summary` exists
  - `routing_decision` exists
  - no escalation reasons
  - no HITL review task
- missing-information case:
  - `disposition == "request_more_information"`
  - `confidence_band == "Medium"`
  - `requirements_checklist` exists
  - `follow_up_message` exists
  - `reviewability_flags` exists
  - `escalation_reasons == []`
- ambiguous case:
  - `disposition == "escalate_to_human_review"`
  - `confidence_band == "Low"`
  - `hitl_review_task` exists
  - `escalation_reasons` exist
  - `escalation_rationale` exists
- governance / scope:
  - raw PII never crosses the external model boundary
  - stable safe tokens are used
  - outputs do not imply adjudication or benefit determination
- evaluation:
  - fake evaluation recorder records all three representative cases

## Assertions Intentionally Weakened Because Of Deferred Hardening

- Replace the exact `"empathetic"` quality-marker assertion with weaker bounded assertions:
  - follow-up message exists
  - follow-up message is non-empty
  - follow-up message remains non-adjudicative
  - optional: follow-up message references the missing items

Reason:

- exact claimant-tone markers are explicitly deferred in `plan/death-claim/deferred-hardening.md`

## Test Plan

Implement in this order:

1. create the fixture directories and representative case bundles
2. add fixture loaders that hydrate `ClaimIntakeBundle` objects from those files
3. add fake collaborator fixtures:
   - `fake_policy_lookup`
   - `fake_document_store`
   - `fake_review_queue`
   - `fake_pii_guardrail`
   - `fake_evaluation_recorder`
   - `triage_workflow`
4. write `test_death_claim_intake_triage.py` as the promoted version of the workshop-spec sketch
5. make the test run under the repo's async pytest setup
6. fill in only the minimum Tree A implementation needed to satisfy the contract

Acceptance scenarios that must pass:

- Case A complete intake -> `proceed`, `High`
- Case B missing information -> `request_more_information`, `Medium`
- Case C ambiguous / HITL -> `escalate_to_human_review`, `Low`

## Assumptions

- `plan/death-claim/workshop-spec.md` remains the upstream behavior source
- `plan/death-claim/tree-a-code-map.md` is sufficient as the naming and boundary map and does not need trimming first
- the first real acceptance test should stay framework-agnostic even if the runtime implementation uses LangGraph later
- the first real test should use filesystem fixtures so the representative cases remain visible and reviewable in VCS
- exact claimant-tone markers are intentionally deferred, so the first runnable test should not over-specify them
