# Death Claim Triage: Phase 2 Implementation Plan (Deterministic Triage)

## Phase Summary

- **Scenario:** Death Claim Triage (Tree A)
- **Phase Goal:** Build the aggregate nodes (`extract_facts`, `assess_triage`) using our deterministic use cases. Ensure routing logic exactly matches the three canonical fixtures.
- **Status:** awaiting_review

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **Architecture decisions:** `plan/decisions/_langgraph-architecture-decisions.md` (Decision 2 - Aggregate Nodes)
- **Deferred hardening:** `plan/death-claim/deferred-hardening.md` (Granular graph node tracing)
- **Acceptance boundaries:** `tests/acceptance/fixtures/death_claim/*`

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- LLM prompt generation or text sanitization (Phase 3).
- Live API wiring (Phase 4).

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `app/interface_adapters/orchestrators/nodes/extract_facts_node.py` - Wraps extraction.
- `app/interface_adapters/orchestrators/nodes/assess_triage_node.py` - Wraps completeness, ambiguity, and routing.

### Modified Files

- `app/interface_adapters/orchestrators/triage_graph_factory.py` - Wire the new nodes into the graph pipeline and define conditional edge routing based on disposition.

## Assertions & Behavior Contracts

- Use cases must not be embedded directly in the node functions; nodes simply act as thin wrappers formatting the TypedDict context for `app/use_cases/` execution.
- Conditional graph routing edges must strictly depend on the resulting `disposition` state.
- All 3 canonical case paths (proceed, request info, escalate) must correctly resolve their deterministic states.

## Deferred Items Touched (If Any)

| Deferred item                                      | Current assumption used                                                                | Hardening still required                            |
|----------------------------------------------------|----------------------------------------------------------------------------------------|-----------------------------------------------------|
| Granular graph node tracing (1:1 Use Case Mapping) | Nodes are built aggressively aggregating logic (`assess_triage` handles 4+ use cases). | Future breakout for richer observability in Studio. |

## Ordered Implementation Steps

Implement in this order:

1. Build `extract_facts_node.py` pulling logic from Fake Adapters.
2. Build `assess_triage_node.py` running the deterministic checks (Completeness -> Ambiguity -> Reviewability -> Routing).
3. Update `triage_graph_factory.py` to compile `START -> extract_facts -> assess_triage -> END`.
4. Update `tests/unit/app/interface_adapters/orchestrators/` to assert state changes across the nodes.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- State cleanly processes through both aggregate nodes for the 3 representative cases using mocked starting states.
- Conditional edge testing successfully maps `disposition` enum outputs to expected graph branches.

## Assumptions

- We are continuing to assume Fake Adapters guarantee test stability for factual extraction logic at this stage.
