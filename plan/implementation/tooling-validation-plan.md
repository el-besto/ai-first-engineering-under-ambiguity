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

## Assumptions

- durable demo artifacts may live in the repo when created, but there is no separate VCS-tracked demo plan
- if time compresses, preserve the live end-to-end graph, strict tokenization boundary, external LLM artifact generation, and thin API/UI surfaces before attempting the local-SLM stretch path
