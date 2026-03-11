# Death Claim Triage: Phase 1 Implementation Plan (State & Scaffold)

## Phase Summary

- **Scenario:** Death Claim Triage (Tree A)
- **Phase Goal:** Define the `TriageGraphState`, implement the closure-based factory structure for the `AdapterRegistry`, and wire up the basic skeleton using Fake Adapters.
- **Status:** awaiting_review

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **Architecture decisions:** `plan/decisions/_langgraph-architecture-decisions.md` (Decision 1 & Decision 4)
- **Deferred hardening:** `plan/death-claim/deferred-hardening.md` (PII in graph state, Fake Collaborators)

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- Extracting real facts or logic routing (Phase 2).
- PII sanitization or LLM prompt generation (Phase 3).
- Live execution via Streamlit or API (Phase 4).

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `app/interface_adapters/orchestrators/triage_graph_state.py` - TypedDict for accumulation state and mapper to `TriageResult`.
- `app/interface_adapters/orchestrators/triage_graph_factory.py` - Closure/Factory to build the nodes using `AdapterRegistry`.
- `tests/unit/app/interface_adapters/orchestrators/test_triage_graph_state.py` - Validates dict-to-entity mapping.
- `tests/unit/app/interface_adapters/orchestrators/test_triage_graph_factory.py` - Validates dependency injection wiring.

### Modified Files

- `plan/implementation/langgraph-live-model-plan.md` - (To be deleted, replaced by these mapped phases).

## Assertions & Behavior Contracts

- Graph state must be a `TypedDict` using primitives or known dataclasses to allow predictable LangGraph reduction.
- Dependency injection must not live inside graph nodes directly; nodes must be constructed via factory closures over the `AdapterRegistry`.
- PII is temporarily permitted in the `TriageGraphState` (per deferred hardening).

## Deferred Items Touched (If Any)

| Deferred item                   | Current assumption used                                                      | Hardening still required                  |
|---------------------------------|------------------------------------------------------------------------------|-------------------------------------------|
| Strict runtime state validation | Ergonomics over strict runtime enforcement using `TypedDict`                 | Pydantic evaluation for state transitions |
| PII in graph state              | Raw PII is permitted to live in the state dict prior to external generation. | Upstream SLM anonymization.               |

## Ordered Implementation Steps

Implement in this order:

1. Delete the obsolete `langgraph-live-model-plan.md` draft.
2. Define the `TriageGraphState` dict in `triage_graph_state.py`.
3. Build the mapping function out to `TriageResult`.
4. Create the `build_triage_graph(adapters: AdapterRegistry)` factory.
5. Create mock placeholder nodes that simply return the state untouched.
6. Write unit tests to prove factory compilation and state mapping.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- `make check` passes with Pyright confirming valid TypedDict structures.
- Unit tests pass demonstrating successful instantiation of a `CompiledGraph`.
- The graph diagram can be rendered or inspected.

## Assumptions

- We are continuing to use Fake adapters for Policy Lookup, Intake, and Review.
