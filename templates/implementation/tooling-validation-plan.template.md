# [Scenario Name]: Tooling Validation Plan

## Summary

Use this document for the local validation posture around the thin PoC slice and
its supporting tooling.

This document owns guardrail, runtime, tooling, and local validation checks
that are broader than the acceptance-driven PoC code path. It does **not** own
fixture authoring or PoC behavior implementation; those remain in the
acceptance-contract plan.

## Current Source Inputs

- Root tracker: `<root_tracker_path>`
- Slice anchor: `<slice_anchor_path>`
- Deferred hardening: `<defer_register_path>`
- Repo patterns: `<repo_patterns_path>`

## Validation Scope

Validate the thin slice with checks for:

- acceptance coverage across all representative cases
- API smoke coverage
- UI smoke coverage
- raw PII never crossing the external model boundary
- stable safe tokens being used before external analysis
- outputs avoiding adjudication, benefit-determination, and payout language
- live-model usefulness under tokenization

## Local Runtime Checks

Run the following local validations once the slice is wired:

- verify debugger attach on `<debug_command>`
- inspect one good local runtime or Studio run for each representative case
- run a light `<compose_validation_command>` validation
- run a light `<local_runtime_validation_command>` validation
- run one late `<late_runtime_validation_command>` validation pass

## Live-Model Validation

Minimum live-model validation:

- at least one successful live external LLM run per representative case
- if time compresses, at minimum one live run per disposition
- confirm tokenization preserves enough referential meaning for useful
  downstream outputs

## Stretch Validation

Optional stretch validation:

- run at least one representative case through the stretch privacy path
- confirm the same downstream flow still works with tokenized entities from that
  path

## Ordered Validation Steps

1. Start with the deterministic acceptance path and confirm all representative
   cases still satisfy the bounded triage contract.
2. Validate the shared workflow path before checking individual surfaces so UI
   and API issues do not hide workflow regressions.
3. Run API smoke coverage for the thin API shell and UI smoke coverage for the
   primary workbench.
4. Verify the privacy boundary explicitly by showing that raw PII never crosses
   the external model boundary and that stable safe tokens are used before
   external analysis.
5. Run the minimum live-model validation pass and confirm tokenization still
   leaves enough referential meaning for useful downstream outputs.
6. Run the local runtime checks for debugger attach, runtime inspection,
   compose, local runtime helpers, and one late validation pass.
7. Attempt the stretch validation only if the core validation path is already
   stable.

## Validation Done Criteria

Validation is complete when:

- the thin slice is stable enough for demo credibility
- guardrail coverage is explicit
- the shared workflow path works through both UI and API
- baseline local runtime and tooling checks have passed at least once

## Out Of Scope

This document does not own:

- demo rehearsal and timing notes
- broader production hardening beyond thin local validation
- fixture creation beyond the validation expectations already owned by the
  acceptance contract

## Verification

Verify the validation pass with evidence that:

- all representative cases pass through the acceptance boundary
- both UI and API exercise the same shared workflow path
- the thin health and primary workflow endpoints behave as expected
- the privacy boundary is inspectable and raw PII is excluded from external
  model-facing input
- live-model validation succeeded for each representative case, or for each
  disposition if time compressed
- local runtime checks completed at least once

## Completion Report

Report the following at the end of a validation pass:

- checks run and their results
- which representative cases and dispositions were validated live
- evidence used to confirm the privacy boundary
- any failures, flaky behaviors, or demo-credibility risks that remain
- any skipped checks and why they were skipped
- whether the slice is ready to move on or needs another stabilization pass

## Assumptions

- durable demo artifacts may live in the repo when created, but there is no
  separate VCS-tracked demo plan
- if time compresses, preserve the live end-to-end workflow, strict tokenization
  boundary, external LLM artifact generation, and thin UI/API surfaces before
  attempting the stretch privacy path
