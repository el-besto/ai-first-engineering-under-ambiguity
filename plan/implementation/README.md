# Implementation Control

This directory holds the **live implementation-control documents** for the current PoC.

Working split:

- [`../../PROJECT_PLAN.md`](../../PROJECT_PLAN.md)
  - repo-level assignment framing, deliverables, and progress
- `plan/death-claim/`
  - defines what the slice must do
  - source-of-truth scenario and design inputs
- `plan/implementation/`
  - tracks how the current implementation pass is turning that into code
  - separates one-time setup/bootstrap from the acceptance-driven PoC code path
- `templates/implementation/`
  - reusable scaffolding for future implementation passes

Current implementation order:

1. repo bootstrap and local scaffold
2. fixture contract and acceptance path
3. workflow facade / orchestration
4. entities, use cases, and fake adapters
5. UI and API surfaces
6. tooling and local validation

Current live documents:

- `change-reports/`

Completed documents:

- `completed/repo-bootstrap-plan.md`
  - scaffold, tooling, local runtime, and privacy-seam bootstrap
- `completed/acceptance-contract-plan.md`
  - fixture-driven PoC code-path implementation plan
- `completed/langgraph-phase-1-state.md`
  - TriageGraphState and factory initialization
- `completed/langgraph-phase-2-deterministic-triage.md`
  - extraction and triage routing nodes
- `completed/langgraph-phase-3-privacy-and-generation.md`
  - PII guardrail and artifact generation nodes
- `completed/langgraph-phase-4-live-model-wiring.md`
  - live model adapter and dependency injection
- `completed/langgraph-phase-5-prompts-and-parsers.md`
  - DSPy prompt templates and Pydantic output parsers
- `completed/langgraph-phase-6-surfaces.md`
  - FastAPI and Streamlit integrations
- `completed/tooling-validation-plan.md`
  - validation posture for tooling, guardrails, and thin local runtime checks

Use `change-reports/` for substantial autonomous or semi-autonomous implementation passes after code starts landing.
