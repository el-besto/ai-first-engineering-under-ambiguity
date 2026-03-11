# DSPy Guardrail: Phase 1 Implementation Plan (Compilation)

## Phase Summary

- **Feature:** Local SLM PII Guardrail
- **Phase Goal:** Establish the local MLOps pipeline to compile an optimized DSPy signature for PII extraction using a local SLM, proving the viability of the Vaultless PII Guardrail.
- **Status:** ready (stretch goal)

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **Architecture decisions:** `plan/decisions/_langgraph-architecture-decisions.md` (Decision 4 - Privacy Bound)
- **Technical Architecture:** `plan/technical/pii-guardrail-architecture.md`
- **Reference Code:** `plan/technical/pii-guardrail-code-reference.md`
- **Deferred hardening:** `plan/death-claim/deferred-hardening.md` (Stretch Goal boundary)
- **Acceptance test boundary:** `tests/acceptance/features/test_death_claim_intake_triage.py`

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- Integrating the compiled DSPy model into the active LangGraph runtime (reserved for Phase 8).
- Running the `BootstrapFewShot` compilation during live API requests (this phase builds the offline compilation script only).

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `scripts/compile_dspy_guardrail.py` - Offline script to define the training set, run `BootstrapFewShot`, and save the optimized prompt weights.
- `app/adapters/safety/dspy_signatures.py` - Contains the `ExtractPII` signature and the `pii_metric` focused on 100% recall.
- `tests/unit/test_dspy_metrics.py` - Asserts the custom `pii_metric` behaves correctly (penalizing false negatives aggressively).

### Modified Files

- `deploy/local/compose.yaml` - Add an `ollama` service configuration to run the local SLM.
- `Tiltfile` - Register the `ollama` service so it runs automatically via `tilt up` alongside the UI and API.

## Assertions & Behavior Contracts

- The custom `pii_metric` MUST prioritize recall over precision (score = 0.0 if any ground-truth PII is missed).
- The compilation script must successfully interact with a local SLM configured in `Ollama` via the `dspy` client.
- The compilation output must be a saved artifact that can be loaded quickly at runtime.

## Deferred Items Touched (If Any)

| Deferred item                 | Current assumption used            | Hardening still required   |
|-------------------------------|------------------------------------|----------------------------|
| Local SLM guardrail injection | Stretch goal - currently uses fake | Full integration (Phase 8) |

## Ordered Implementation Steps

Implement in this order:

1. Update `deploy/local/compose.yaml` and `Tiltfile` to include an `ollama` container that pulls and serves `llama3.1:8b` on port `11434`.
2. Create `app/adapters/safety/dspy_signatures.py` with the `ExtractPII` signature and strict recall metric.
3. Create `tests/unit/test_dspy_metrics.py` to prove the metric logic.
4. Author a small, representative few-shot dataset of fake insurance intake snippets inside the compilation script.
5. Build the `scripts/compile_dspy_guardrail.py` to run the `BootstrapFewShot` teleprompter against the local Ollama endpoint.
6. Successfully run the compiler script and observe the optimized prompt parameters.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- The unit tests for `pii_metric` pass.
- A local execution of `scripts/compile_dspy_guardrail.py` completes without errors and outputs a saved DSPy optimization trace.

## Assumptions

- The host machine has sufficient capacity (RAM/GPU) to run the Llama 3.1 8B parameter model locally via the new Docker container.
