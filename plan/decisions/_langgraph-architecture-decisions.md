# LangGraph Integration for Death Claim Triage: Decisions Needed

> **Template Version:** 1.0 (2025-10-13)
>
> **Usage Instructions:** See `templates/decision/decision-document-template.README.md` for how to use this template and how it fits into the repo's decision-record workflow.
>
> **Related Template:** Use this document when a cross-cutting repo or implementation decision needs explicit options, rationale, and status tracking.

---

**Status:** 🚧 0 of 5 Resolved | 5 Awaiting Discussion

This document captures the key architectural decisions required to transition our deterministic triage facade into a live LangGraph workflow (Block 4 of the PoC plan) while preserving our exact testing contracts.

**Update:** Initial decisions drafted based on the existing `TriageOrchestrator` contract.

---

## Decision 1: Graph State Shape ⚠️

**What I did:**

- Evaluated LangGraph's requirement for a defined `State` object passed between nodes.
- Reviewed our existing `ClaimIntakeBundle` and `TriageResult` entities to see if they fit LangGraph's reduction pattern natively.

**Context:**
The core of a LangGraph workflow is the state dictionary. We need a structure that allows both inputs and progressive outputs to accumulate.

**Question for you:**
What schema should we use for the LangGraph `State`?

- [x] **Option A: Flat TypedDict (Accumulation State)**
  - State is a dictionary containing the bundle, flags (e.g., `is_complete`), facts, and generated artifacts. It maps to `TriageResult` only at the very end.
  - ✅ Pro: Very native to LangGraph's standard reduction pattern.
  - ✅ Pro: Easy to inspect visually in LangGraph Studio.
  - ❌ Con: Requires mapping standard entities in and out of the graph boundary.

- [ ] **Option B: Entity-Backed State**
  - State holds the exact `ClaimIntakeBundle` object and a progressively built `TriageResult` object.
  - ✅ Pro: Reuses our exact domain objects natively inside nodes.
  - ❌ Con: Mutating rich Python objects inside a LangGraph state can sometimes cause tracking/checkpointing friction compared to primitive dicts.

- [ ] **Option C: Pydantic BaseModel State**
  - State is defined as a Pydantic `BaseModel` that enforces strict schema validation on every node update.
  - ✅ Pro: Strong runtime typing and schema guarantees.
  - ❌ Con: Can be heavy for partial accumulation updates; might require custom reducers to avoid overwriting attributes.

**My recommendation:** Option A

**Reasoning:**
A flat `TypedDict` accumulates facts predictably. LangGraph Studio rendering works best when state values are simple primitives or standard dicts rather than deeply nested custom instances. We can keep the architectural boundary clean by mapping the final state dict back into our `TriageResult` domain entity right before returning to the caller.

**Your decision:** Option A

**Rationale:**
As per `docs/patterns.md`, entities are immutable by default (`frozen=True`). A flat `TypedDict` for the graph state that accumulates facts and maps back to the `TriageResult` at the edge is the most ergonomic approach for LangGraph without constantly recreating full domain entities inside nodes. PII is temporarily allowed in this state (see Decision 5 and deferred hardening).

**Impact:** HIGH - Defines how data moves through every node in the graph.

**Status:** ✅ RESOLVED

---

## Decision 2: Node Topology

**What I did:**

- Reviewed the 8 existing Use Cases inside the `TriageOrchestrator` facade to identify logical graph node boundaries.

**Context:**
Granular nodes (1 use case = 1 node) provide maximum visibility but can clutter the visual graph. Aggregate nodes (multiple use cases = 1 node) simplify the graph but hide internal rules.

**Question for you:**
How aggressively should we group Use Cases into graph nodes?

- [x] **Option A: Aggregate Nodes by Phase**
  - Create 3-4 nodes: `extract_facts`, `assess_triage`, `generate_artifacts`.
  - ✅ Pro: Creates a very clean, easy-to-read top-level graph.
  - ❌ Con: Hides the discrete logic separation inside the nodes.

- [ ] **Option B: 1:1 Mapping (Granular)**
  - A distinct node for `normalize`, `extract`, `assess_completeness`, `detect_ambiguity`, etc.
  - ✅ Pro: Maximum granularity and step-level tracing in Langsmith/Studio.
  - ❌ Con: The graph visual layout becomes very long and linear before any branching.

- [ ] **Option C: Subgraphs per Phase**
  - A top-level graph of 3-4 phases, where each node calls a localized subgraph mapping perfectly to the 1:1 Use Cases.
  - ✅ Pro: Best of both worlds—clean top-level abstraction with granular tracing beneath.
  - ❌ Con: Significant structural overhead and code complexity for a simple 3-case PoC.

**My recommendation:** Option A

**Reasoning:**
Given the 5-minute demo constraint, explaining a massive 12-node graph is harder than explaining a 4-phase graph with clear conditional edges. Grouping deterministic rule executions (like completeness and ambiguity checks) into a single `assess_triage` block feels pragmatically clear.

**Your decision:** Option A

**Rationale:**
A simple, high-level graph of 3-4 phases (`extract_facts`, `assess_triage`, `generate_artifacts`) aligns with the need for a clean, 5-minute demonstrable visual structure in Studio. It keeps the top-level flow legible while wrapping the deterministic use cases cleanly within those phases.

**Impact:** MEDIUM - Primarily affects visual presentation in Studio/LangSmith.

**Status:** ✅ RESOLVED

---

## Decision 3: LLM Integration Strategy ⚠️

**What I did:**

- Identified which operations require semantic reasoning vs deterministic checks to maintain the acceptance suite passing status.

**Context:**
We want the demo to show tangible LLM capabilities without risking non-deterministic routing for critical triage constraints (e.g., missing signature = request info).

**Question for you:**
Which nodes should transition to live LLM calls in this slice?

- [ ] **Option A: LLM Artifact Generation Only**
  - Fact extraction and disposition routing remain deterministic rules. Only the artifact generation (checklists, empathetic messages, rationales) utilize Langchain LLM calls.
  - ✅ Pro: Guarantees routing aligns perfectly with acceptance tests.
  - ✅ Pro: Shows off LLM synthesis and tone manipulation safely.
  - ❌ Con: Fact extraction (reading the document) remains mocked.

- [ ] **Option B: LLM Fact Extraction + LLM Generation**
  - The LLM extracts the `[MISSING]` tags and generates the responses. Routing logic remains deterministic based on the LLM's structured output.
  - ✅ Pro: Slightly more realistic demonstration of AI reading the document.
  - ❌ Con: Higher risk of test flakiness if the LLM hallucinating facts causes the wrong disposition.

- [ ] **Option C: LLM Agentic Routing + Generation**
  - Provide the LLM with the raw claim bundle and allow it to actively decide the disposition alongside artifact generation.
  - ✅ Pro: Fully "agentic" workflow showing deep LLM control.
  - ❌ Con: Extremely brittle; almost guaranteed to violate the rigid `acceptance-contract-plan` assertions.

**My recommendation:** Option A

**Reasoning:**
The 15-hour plan constrained the scope to prioritize safety boundaries over pipeline realism. Deterministic fact extraction keeps our test suite unconditionally green.

**Your decision:** Option A

**Rationale:**
Strictly enforced by `docs/patterns.md` (Section 7.1). Deterministic routing, completeness, and ambiguity policy must stay outside the model. External LLM calls are reserved exclusively for bounded artifact generation. This guarantees our deterministic test paths remain unconditionally green.

**Impact:** CRITICAL - Defines the boundary between deterministic rules and stochastic models.

**Status:** ✅ RESOLVED

---

## Decision 4: Adapter Injection

**What I did:**

- Evaluated LangGraph's ConfigurableField vs Python closures for dependency injection inside nodes.

**Context:**
We must use Fake adapters in our Pytest suite, but real Langchain wrappers in our FastAPI/Streamlit apps.

**Question for you:**
How do we inject dependencies into the LangGraph state/nodes?

- [ ] **Option A: Graph Configuration (ConfigurableField)**
  - Pass the LLM client and mocks through LangGraph's `RunnableConfig`.
  - ✅ Pro: Native to LangGraph's intended configuration injection.
  - ❌ Con: Can be clunky for rich object dependencies compared to simple strings.

- [x] **Option B: Closure / Factory Wrapping**
  - Build the nodes dynamically inside a factory function that closes over the supplied `AdapterRegistry`.
  - ✅ Pro: Very clean Pythonic dependency injection.
  - ❌ Con: Recompiles the graph diagram object every time the factory is called if not cached.

- [ ] **Option C: Context Variables (ContextVars)**
  - Set the adapters on global async-safe `contextvars` before executing the graph, which internal use cases read.
  - ✅ Pro: Leaves the graph node signatures completely unaffected.
  - ❌ Con: Seen as an anti-pattern for testing; hides data flow compared to explicit injection.

**My recommendation:** Option B

**Reasoning:**
Python closures over an `AdapterRegistry` keep the node functions pure relative to their injected dependencies without wrestling with `RunnableConfig` typing.

**Your decision:** Option B

**Rationale:**
Aligns with `docs/patterns.md` (Section 4.5), which dictates manual wiring from driver dependency modules. Python closures/factory wrapping provide explicit dependency injection into the graph without relying on LangGraph-specific configuration constructs (`RunnableConfig`) or implicit context variables, keeping the domain/use-case layers clean.

**Impact:** HIGH - Dictates the architectural seam of the entire application.

**Status:** ✅ RESOLVED

---

## Decision 5: Privacy Boundary Placement ⚠️

**What I did:**

- Mapped the requirement that raw PII never crosses external boundaries to potential topological edges in the graph.

**Context:**
Raw PII must never reach the `generation_node`.

**Question for you:**
How is the `PIIGuardrailAdapter` surfaced in the graph topology?

- [x] **Option A: Explicit `tokenize_pii` Node**
  - PI tokenization is its own node in the graph, visibly running before the conditional LLM edge.
  - ✅ Pro: Makes the privacy boundary explicitly visible in the demo/Studio.
  - ❌ Con: One extra graph transition step.

- [ ] **Option B: Internal to the Generation Node**
  - Tokenization happens invisibly at the exact moment the LLM is called.
  - ✅ Pro: Simpler graph.
  - ❌ Con: Hides the privacy boundary from the stakeholders observing the trace.

- [ ] **Option C: Pre-Graph Middleware**
  - Tokenize the entire `ClaimIntakeBundle` before it even enters the graph state.
  - ✅ Pro: Absolute guarantee no PII can leak into the graph.
  - ❌ Con: Makes graph logic much harder if it needs to evaluate original data for non-external reasons (like policy lookup mapping).

**My recommendation:** Option A

**Reasoning:**
The plan dictates that privacy is a first-class citizen of this demo. An explicit graph node running prior to any LLM node visually guarantees that the PII was handled properly in the execution trace.

**Your decision:** Option B (Modified/Deferred)

**Rationale:**
While `docs/patterns.md` (Section 7.4) strictly prohibits raw PII in graph state, we are intentionally deferring this strict enforcement for the initial PoC slice to maintain a workable abstraction layer and secure easy wins. PII will be allowed in the graph state temporarily. The privacy boundary will be enforced via the `PIIGuardrailAdapter` immediately prior to any external LLM call (effectively grouping it internally or immediately prior to the generation node). A risk register item has been added to `plan/death-claim/deferred-hardening.md` to track the eventual removal of raw PII from the graph state once the local SLM sanitization is implemented.

**Impact:** CRITICAL - Demonstrates adherence to strict governance requirements, with an explicit, tracked deferral.

**Status:** ✅ RESOLVED

---

## Summary Of Decisions

| # | Decision                   | Priority | Status     |
|---|----------------------------|----------|------------|
| 1 | Graph State Shape          | HIGH     | ✅ RESOLVED |
| 2 | Node Topology              | MEDIUM   | ✅ RESOLVED |
| 3 | LLM Integration Strategy   | CRITICAL | ✅ RESOLVED |
| 4 | Adapter Injection          | HIGH     | ✅ RESOLVED |
| 5 | Privacy Boundary Placement | CRITICAL | ✅ RESOLVED |

---

## Next Steps

**Completed:**

- ✅ Drafted decision questions based on `TriageOrchestrator` conversion requirements.
- ✅ Reviewed relevant `PROJECT_PLAN.md` and `.scratch/PLAN_HUMAN_FINAL.md` documentation to align constraints.

1. Update `plan/implementation/langgraph-live-model-plan.md` with execution tasks based on these choices.
2. Adjust `PROJECT_PLAN.md` progress tracker.
3. Begin Block 4 integration against our test suite.

**Status:** 5 of 5 decisions resolved

---

## Notes

**Decision Discovery Process:**

- These architectural integration decisions were identified by matching the completed `acceptance-contract-plan.md` outputs with the required Block 4 "live LangGraph" deliverables outlined in `.scratch/PLAN_HUMAN_FINAL.md`.

**Related Documents:**

- [PROJECT_PLAN.md](../../PROJECT_PLAN.md)
- [PLAN_HUMAN_FINAL.md](../../.scratch/PLAN_HUMAN_FINAL.md)
