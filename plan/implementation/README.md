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

<!-- AGENT: List active implementation plans here. Use `- none` if empty. -->
- none

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
- `completed/langgraph-phase-7-live-e2e-tests.md`
  - live E2E model tests via Pytest
- `completed/langgraph-phase-7-validation-plan.md`
  - validation posture for Phase 7 E2E live tests
- `completed/dspy-guardrail-phase-1-compilation.md`
  - local SLM offline prompt Compilation
- `completed/dspy-guardrail-phase-2-integration.md`
  - Vaultless PII Guardrail runtime integration
- `completed/dspy-guardrail-phase-3-live-e2e-tests.md`
  - live E2E model tests for SLM + Guardrail + OpenAI
- `completed/dspy-guardrail-validation-plan.md`
  - validation posture for DSPy Guardrail integration
- `completed/langgraph-phase-8-composable-artifact-nodes-and-pii-audit.md`
  - Composable Artifact Nodes and PII Audit
- `completed/langgraph-phase-8-validation-plan.md`
  - validation posture for Phase 8 Composable Artifact Nodes and PII Audit
