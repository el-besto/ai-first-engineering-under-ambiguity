# LangGraph Phase 8 Validation Plan: Composable Artifact Nodes and PII Audit

## Summary

Use this document for the local validation posture around the thin PoC slice and
its supporting tooling introduced during **Phase 8 (Composable Artifact Nodes and PII Audit)**.

This document owns guardrail, runtime, tooling, and local validation checks
that are broader than the acceptance-driven PoC code path. It does **not** own
fixture authoring or PoC behavior implementation; those remain in the
acceptance-contract plan.

## Current Source Inputs

- Root tracker: `plan/death-claim/steel-thread.md`
- Slice anchor: `plan/implementation/completed/langgraph-phase-8-composable-artifact-nodes-and-pii-audit.md`
- Deferred hardening: `plan/death-claim/deferred-hardening.md`
- Repo patterns: `docs/patterns.md`

## Validation Scope

Validate the thin slice with checks for:

- acceptance coverage across all representative cases (Complete, Missing Info, Ambiguous)
- API smoke coverage
- UI smoke coverage (specifically the Triage Workbench)
- the visual validation of the new static graph topology map rendering
- raw PII never crossing the external model boundary (truthful audit panel verification)
- tokenized model inputs remaining isolated from deterministic internal logic state
- outputs avoiding adjudication, benefit-determination, and payout language
- live-model usefulness under tokenization for generated artifacts (Summary, Checklist, Follow-up, Rationale)
- structural logging conformance for all newly introduced and modified surfaces

## Local Runtime Checks

Run the following local validations once the slice is wired:

- verify debugger attach via your IDE on `make run-cli` or `uv run pytest`
- have the AI Agent inspect one good local runtime run for each representative case using the Streamlit UI (`make ui`) via its browser tool
- visually inspect the terminal output for the new structured logging formatting and lack of PII leakage
- run a light `make lint` and `make typecheck` validation pass
- run a late `pytest tests/acceptance/` validation pass to ensure core abstractions have not regressed

## Live-Model Validation

Minimum live-model validation (requires a valid `LLM_MAIN_API_KEY`):

- at least one successful live external LLM run per representative case in the Streamlit UI
- confirm tokenization preserves enough referential meaning for useful downstream outputs (e.g. summaries and checklists are still coherent despite scrubbed PII)
- at least one successful live external LLM run per representative case in the Streamlit UI, exercised and visually verified by the AI Agent

## Stretch Validation

Optional stretch validation:

- Attempt to run the components independently via lower-level CLI or script usage outside of Streamlit.
- Provide a deliberately malformed bundle to test error paths and verify that the `log_exception` structured logging correctly renders the stack trace and derived variables.

## Ordered Validation Steps

1. Start with the deterministic acceptance path (`uv run pytest tests/acceptance`) and confirm all representative cases still satisfy the bounded triage contract.
2. Verify structural logging changes by running a CLI command like `uv run python -m drivers.cli.main graph run MISSING` and ensuring standard structlog formatting appears explicitly showing component + operation binding.
3. Validate the shared workflow path by booting the UI (`make ui`).
4. In the UI, the AI Agent must use its browser tool to run the **Complete Claim** scenario. Verify that the disposition panel correctly shows the outcome, the audit panel correctly compares the original and scrubbed text, and the topology panel successfully renders the Mermaid PNG static map.
5. Verify the privacy boundary explicitly by ensuring the **Security Audit** panel shows the _actual_ `tokenized_document_facts` payload used by the generated branches, not just a relabelled presentation of raw text.
6. Run the **Missing Info** and **Ambiguous Scenario** flows in the UI via the AI Agent to ensure the respective new branches (`generate_missing_info_artifacts`, `generate_hitl_artifacts`) execute correctly and utilize the tokenized state for LLM generation.
7. Confirm through the returned artifacts in the app UI that tokenization still leaves enough referential meaning for useful downstream outputs.
8. Run the local standard CI simulation checks (`make test`, `make lint`, `make typecheck`).

## Validation Done Criteria

Validation is complete when:

- the Phase 8 topological changes run stably without crashing
- the Streamlit UI truthful audit explicitly shows the tokenized boundary
- the topology UI accurately renders the static Mermaid map
- all three branch generation nodes work for their respective scenarios
- logs exclusively use standard bounded telemetry without PII leakage
- baseline local runtime and internal CI checks pass

## Out Of Scope

This document does not own:

- demo rehearsal and timing notes
- broader production hardening beyond thin local validation
- fixture creation beyond the validation expectations already owned by the
  acceptance contract

## Verification

Verify the validation pass with evidence that:

- all representative cases pass through the acceptance boundary.
- the topology panel visibly maps the execution state via a static image during a live run.
- the privacy boundary is inspectable in the UI and raw PII is demonstrably excluded from external model-facing input.
- live-model validation succeeded for each branch disposition.
- local tooling runs (lint, typecheck, test) succeed.

## Completion Report

Report the following at the end of a validation pass:

- checks run and their results
- which representative cases and dispositions were validated live
- evidence used to confirm the privacy boundary (e.g. screenshots of the Security Audit UI tab)
- screenshot of the new Static Graph Topology rendering
- any failures, flaky behaviors, or demo-credibility risks that remain
- any skipped checks and why they were skipped
- whether the slices are ready for main or need further stabilization

## Assumptions

- durable demo artifacts may live in the repo when created, but there is no separate VCS-tracked demo plan
- if time compresses, prioritize the UI-based Live-Model Validation and the Acceptance tests over stretch CLI/error path validations.
