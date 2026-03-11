# Death Claim Triage: Phase 3 Implementation Plan (Privacy & Generation)

## Phase Summary

- **Scenario:** Death Claim Triage (Tree A)
- **Phase Goal:** Implement the `tokenize_pii` pre-model guardrail node, and build the `generate_artifacts` node with a Fake Model adapter to prove the pipeline securely.
- **Status:** awaiting_review

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Architecture decisions:** `plan/decisions/_langgraph-architecture-decisions.md` (Decision 3 - Generation Only, Decision 5 - Middleware Boundary)
- **Deferred hardening:** `plan/death-claim/deferred-hardening.md` (LLM Fact Extraction Deferred)
- **Privacy requirements:** PII must never cross the external model boundary.

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- Extracting facts via LLMs (we strictly generate artifacts based on deterministic extraction).
- Live OpenAI/LLM provider calls (Phase 4).

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `app/interface_adapters/orchestrators/nodes/tokenize_pii_node.py` - Wraps `PIIGuardrailAdapter`.
- `app/interface_adapters/orchestrators/nodes/generate_artifacts_node.py` - Coordinates LLM artifact requests (Checklists, Tone, Summary).

### Modified Files

- `app/interface_adapters/orchestrators/triage_graph_factory.py` - Compiles the full conditional pipeline (incorporating PIIGuardrail and Artifact boundaries).

## Assertions & Behavior Contracts

- Graph telemetry/traces must not leak raw PII *after* the `tokenize_pii_node`.
- Generation nodes must strictly rely on the Fake Model adapter for pipeline verification.
- Artifact Generation MUST be isolated to the exact use cases specified (Summary, FollowUp, Routing Checklist).

## Deferred Items Touched (If Any)

| Deferred item                                          | Current assumption used                                                                                             | Hardening still required                             |
|--------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| PII in graph state and `PIIGuardrailAdapter` placement | `tokenize_pii` graph node explicitly strips PII before any subsequent nodes can access the external model boundary. | Moving tokenization to local SLM entirely pre-graph. |
| LLM Fact Extraction + LLM Generation                   | Artifact generation only.                                                                                           | Leverage local SLM for true AI extraction post-PoC.  |

## Ordered Implementation Steps

Implement in this order:

1. Implement `tokenize_pii_node.py` injecting `PIIGuardrailAdapter`.
2. Implement `generate_artifacts_node.py` injecting `ModelAdapter`.
3. Update `triage_graph_factory.py` topology (`assess_triage` -(if proceed)-> `tokenize_pii` -> `generate_artifacts`).
4. Validate Fake Model adapter structure returns proper string constants for our tests.

## Verification Plan

Verify the completion of this phase with evidence that:

- Fake Model outputs populate the state correctly.
- Tokens (not names or explicit SSNs) map over the model boundary during trace assertions.

## Assumptions

- We are relying on `ModelAdapter.fake.py` entirely for this phase validation.
