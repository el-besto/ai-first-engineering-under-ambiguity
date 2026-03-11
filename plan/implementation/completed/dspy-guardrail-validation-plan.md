# DSPy Guardrail: Tooling Validation Plan (DSPy Guardrails)

## Summary

Use this document for the local validation posture around the target stretch goals involving DSPy Guardrails and live model testing.

This document serves as a single checkpoint and final regression suite for the DSPy Vaultless FPE tokenization and live SLM model interactions. It captures DSPy Guardrail Phases 1 through 3 in separate, ordered sections. (Note: LangGraph Phases 5-6 are already covered by the core `tooling-validation-plan.md`).

## Current Source Inputs

- Root tracker: `plan/death-claim/workshop-spec.md`
- Slice anchor: `tests/acceptance/features/test_death_claim_intake_triage.py`
- DSPy Phases:
  - `plan/implementation/completed/dspy-guardrail-phase-1-compilation.md`
  - `plan/implementation/completed/dspy-guardrail-phase-2-integration.md`
  - `plan/implementation/completed/dspy-guardrail-phase-3-live-e2e-tests.md`

## Validation Scope

Validate the expanded thin slice with checks for:

- **DSPy Guardrail Compilation (Phase 1):** The offline script compiles an optimized prompt against a local SLM prioritizing 100% PII recall.
- **DSPy Integration (Phase 2):** Vaultless FPE correctly encrypts PII deterministically (`TOK-...`) before external LLM interaction, and fully decrypts it downstream.
- **Live Guardrail Testing (DSPy Phase 3):** Fully integrated tests communicate with external APIs (OpenAI) and local containerized models (Ollama) without manual interaction, demonstrating the privacy bounds specifically for the vaultless token translation.

## Local Runtime Checks

Run the following local validations once the slice is wired:

- Ensure the `ollama` container is running and healthy with the target SLM.
- Inspect one good local runtime execution of `scripts/compile_dspy_guardrail.py` to ensure it interacts with the SLM and saves a trace.

## Live-Model Validation

Minimum live-model validation:

- Ensure the combined SLM + LLM test (`test_live_dspy_e2e_triage.py`) successfully roundstrips PII into vaultless tokens and translates them back into cleartext artifacts downstream.
- Confirm tokenization preserves enough referential meaning for the generation model to return useful outputs.

## Organized Validation Sections

### Section 1: Vaultless Guardrail Compilation & Integration (DSPy Phases 1 & 2)

1. Run the DSPy compilation script against the local Llama SLM. Verify the `pii_metric` correctly penalizes false negatives.
2. Ensure the resulting DSPy optimization trace is stored as a loadable artifact.
3. Run standard acceptance tests (`make test`) with the `VaultlessPIIGuardrail` integrated.
4. Verify the `TriageGraphState` contains `TOK-...` base64 strings and successfully reverses them prior to final response generation.

### Section 2: Targeted System Regression

Because integrating the live DSPy SLM and AES-GCM encryption replaces the deterministic fake guardrail with a true cryptographic tokenization engine, the upstream delivery surfaces and acceptance paths MUST be re-verified to guarantee the core system contract holds:

1. **Core Acceptance Regression:** Re-run the standard deterministic acceptance suite (`make test`) explicitly ensuring the `VaultlessPIIGuardrail` successfully roundstrips without breaking the 3 canonical triage paths.
2. **UI Regression:** Launch the Streamlit workbench (`make ui`) and manually inspect the Token Audit Panel for the "Complete" and "Ambiguous" fixtures, ensuring the new `TOK-...` encryption values render cleanly and the PII boundary remains visually sound.
3. **Graph State Regression:** Inspect a local Studio or debug trace verifying that raw cleartext PII is still flawlessly restored in the final downstream node state before the API response is served.

### Section 3: Live Guardrail Validation (DSPy Phase 3)

1. Supply live credentials (`LLM_MAIN_API_KEY`) in your local `.env`.
2. Run the live DSPy E2E tests (`pytest -m live`) to validate the full end-to-end Vaultless Guardrail cryptography round-trip against the live OpenAI environment.

## Validation Done Criteria

Validation is complete when:

- The `VaultlessPIIGuardrail` uses AES-GCM encrypted deterministic tokens integrated with the compiled DSPy model.
- Live End-to-End tests execute cleanly, proving data remains secure at the LLM boundary and cleartext is accurately restored.
- The local SLM accurately extracts PII without fatal omissions.
- The targeted upstream delivery surfaces (UI Audit Panel, Core API paths) continue to function identically with the live tokens.

## Out Of Scope

This document does not own:

- Demo rehearsal and timing notes.
- Broader production hardening beyond thin local validation.
- Extensive fixture creation beyond the validation expectations of the acceptance contract.
- Live End-to-end Testing of the generation graph without the local DSPy Vaultless SLM (This belongs in Phase 7 validation).
- Initial validation of the API, UI surfaces, and Prompt Engineering schemas (these are owned by the core `tooling-validation-plan.md`, though their regression under DSPy tokenization *is* owned here).

## Verification

Verify the validation pass with evidence that:

- A local DSPy compilation run generated a successful optimization trace without errors.
- The Vaultless tokens are successfully reversed in local test assertions.
- The Streamlit Token Audit panel successfully mounts and displays the new live-encrypted tokens.

## Completion Report

Report the following at the end of a validation pass:

- Checks run and their results by Section (1 and 2).
- Any failures, flaky behaviors, or demo-credibility risks that remain.
- Whether the slice is ready for final presentation or needs another stabilization pass.

## Assumptions

- If time compresses, ensure the core workflow and the basic tokenization boundary (Phases 5, 6) are thoroughly verified by their respective plans before prioritizing the local DSPy SLM automation (DSPy Phases 1-3).
