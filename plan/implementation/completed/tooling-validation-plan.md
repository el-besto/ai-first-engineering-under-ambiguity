# Death-Claim: Tooling Validation Plan

## Summary

Use this document for the local validation posture around the thin PoC slice and its supporting tooling.

This document owns guardrail, runtime, tooling, and local validation checks that are broader than the acceptance-driven PoC code path. It does **not** own fixture authoring or PoC behavior implementation; those remain in [acceptance-contract-plan.md](./acceptance-contract-plan.md).

## Current Source Inputs

- Root tracker: [../../PROJECT_PLAN.md](../../PROJECT_PLAN.md)
- Slice anchor: [../death-claim/steel-thread.md](../death-claim/steel-thread.md)
- Deferred hardening: [../death-claim/deferred-hardening.md](../death-claim/deferred-hardening.md)
- Repo patterns: [../../docs/patterns.md](../../docs/patterns.md)

## Validation Scope

Validate the thin slice with checks for:

- acceptance coverage across all 3 representative cases
- API smoke coverage
- UI smoke coverage
- raw PII never crossing the external model boundary
- stable safe tokens being used before external analysis
- outputs avoiding adjudication, benefit-determination, and payout language
- live-model usefulness under tokenization

## Local Runtime Checks

Run the following local validations once the slice is wired:

- verify VS Code debugger attach on `langgraph dev --debug-port 5678`
- inspect one good local Studio run for each representative case
- run a light `docker compose` validation
- run a light Tilt validation
- run one `langgraph up` validation pass near the end

## Live-Model Validation

Minimum live-model validation:

- at least one successful live external LLM run per representative case
- if time compresses, at minimum one live run per disposition
- confirm tokenization preserves enough referential meaning for useful downstream outputs

## Stretch Validation

Optional stretch validation:

- run at least one representative case through the DSPy plus local-SLM guardrail path
- confirm the same downstream graph still works with tokenized entities from that path

## Ordered Validation Steps

1. Start with the deterministic acceptance path and confirm all three representative cases still satisfy the bounded triage contract.
2. Validate the shared graph-owned path before checking individual surfaces so UI and API issues do not hide workflow regressions.
3. Run API smoke coverage for the thin FastAPI shell and UI smoke coverage for the Streamlit workbench.
4. Verify the privacy boundary explicitly by showing that raw PII never crosses the external model boundary and that stable safe tokens are used before external analysis.
5. Run the minimum live-model validation pass and confirm tokenization still leaves enough referential meaning for useful downstream outputs.
6. Run the local runtime checks for debugger attach, Studio inspection, `docker compose`, Tilt, and one late `langgraph up` pass.
7. Attempt the DSPy plus local-SLM stretch validation only if the core validation path is already stable.

## Validation Done Criteria

Validation is complete when:

- the thin slice is stable enough for demo credibility
- guardrail coverage is explicit
- the shared graph-owned path works through both Streamlit and FastAPI
- baseline local runtime and tooling checks have passed at least once

## Out Of Scope

This document does not own:

- demo rehearsal and timing notes
- broader production hardening beyond thin local validation
- fixture creation beyond the validation expectations already owned by the acceptance contract

## Verification

Verify the validation pass with evidence that:

- all three representative cases pass through the acceptance boundary
- both Streamlit and FastAPI exercise the same graph-owned path
- `GET /health` and the thin `POST /triage` path behave as expected
- the privacy boundary is inspectable and raw PII is excluded from external model-facing input
- live-model validation succeeded for each representative case, or for each disposition if time compressed
- local runtime checks completed at least once for debugger attach, Studio, `docker compose`, Tilt, and `langgraph up`

## Completion Report

Report the following at the end of a validation pass:

- checks run and their results
- which representative cases and dispositions were validated live
- evidence used to confirm the privacy boundary
- any failures, flaky behaviors, or demo-credibility risks that remain
- any skipped checks and why they were skipped
- whether the slice is ready to move on or needs another stabilization pass

## Assumptions

- durable demo artifacts may live in the repo when created, but there is no separate VCS-tracked demo plan
- if time compresses, preserve the live end-to-end graph, strict tokenization boundary, external LLM artifact generation, and thin API/UI surfaces before attempting the local-SLM stretch path
