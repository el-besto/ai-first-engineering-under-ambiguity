# DSPy Guardrail: Phase 2 Implementation Plan (Integration)

## Phase Summary

- **Feature:** Local SLM PII Guardrail
- **Phase Goal:** Integrate the Vaultless Format-Preserving Encryption (FPE) and the compiled DSPy model into the active LangGraph workflow, securely tokenizing PII before external LLM interaction.
- **Status:** ready (stretch goal)

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **Architecture decisions:** `plan/decisions/_langgraph-architecture-decisions.md` (Decision 4 - Privacy Bound)
- **Technical Architecture:** `plan/technical/pii-guardrail-architecture.md`
- **Reference Code:** `plan/technical/pii-guardrail-code-reference.md`
- **Deferred hardening:** `plan/death-claim/deferred-hardening.md`
- **Acceptance test boundary:** `tests/acceptance/features/test_death_claim_intake_triage.py`

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- Re-compiling the DSPy signatures dynamically at runtime (must load the compiled state from DSPy Phase 1).
- Persisting a global database/vault of tokens (we are strictly implementing the *Vaultless* cryptographic approach).
- Altering the core business logic or topology of the `TriageGraph` (the guardrail sits exclusively within the `tokenize_pii` and `generate_artifacts` seams).

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `app/adapters/safety/vaultless_guardrail.py` - Implements `VaultlessPIIGuardrail` using `AESGCM` and deterministic nonce derivation.

### Modified Files

- `app/adapters/safety/pii_guardrail_adapter.py` - Swaps the `FakePIIGuardrail` backing implementation for the live `VaultlessPIIGuardrail` in production paths, but retains the fake for testing.
- `app/config.py` - Adds `LLM_GUARDRAIL_SECRET_KEY` for the AES encryption.
- `plan/death-claim/deferred-hardening.md` - Remove the "Local SLM Guardrail Injection" section as the debt is paid.

## Assertions & Behavior Contracts

- `VaultlessPIIGuardrail.anonymize()` MUST deterministically replace PII extracted by the SLM with `TOK-...` base64 strings.
- The same plaintext entity MUST always derive the exact same token within a session to preserve referential integrity for the commercial LLM.
- `VaultlessPIIGuardrail.de_anonymize()` MUST flawlessly reverse all `TOK-...` strings back to cleartext by decrypting the tokens.

## Deferred Items Touched (If Any)

| Deferred item                 | Current assumption used            | Hardening still required                |
|-------------------------------|------------------------------------|-----------------------------------------|
| Local SLM guardrail injection | Stretch goal - currently uses fake | None - this phase removes the deferral. |

## Ordered Implementation Steps

Implement in this order:

1. Add symmetric cryptography dependency (`cryptography`) to `pyproject.toml`.
2. Implement `app/adapters/safety/vaultless_guardrail.py` with AES-GCM logic.
3. Update `app/config.py` to handle the 32-byte secret key environment variable.
4. Wire the loaded DSPy extractor from DSPy Phase 1 into the `VaultlessPIIGuardrail`.
5. Update `PIIGuardrailAdapter` to construct and delegate to the new vaultless engine.
6. Verify the end-to-end flow with Streamlit to confirm the visual token audit panel displays true AES-backed tokens.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- The 3 canonical fixtures pass the full LangGraph flow.
- A manual inspection of the `TriageGraphState` confirms that NO raw PII exists during the `generate_artifacts` node execution.
- The final outputs successfully revert to cleartext via `de_anonymize`.

## Assumptions

- The host machine has sufficient capacity to run the local SLM concurrently with the PoC server infrastructure.
