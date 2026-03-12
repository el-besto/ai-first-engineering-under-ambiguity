<!-- AGENT INSTRUCTION: You MUST read `templates/implementation/phased-feature-plan.template.README.md` before using this template to create a new phase plan. Do not alter the structure of this document or omit list items unnecessarily. -->
# LangGraph Phase 8: Composable Artifact Nodes and PII Audit Implementation Plan

## Phase Summary

- **Scenario:** Death Claim Triage
- **Phase Goal:** Make the graph more LangGraph-composable and more demo-traceable by splitting branch-specific artifact generation into distinct graph nodes, making the PII audit panel truthful about the tokenized model-boundary payload, adding a lightweight in-app static graph topology Map, and keeping all new/modified graph and UI surfaces aligned with the repo’s current structured logging conventions.
- **Status:** awaiting_review

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **Architecture decisions:** `plan/decisions/_observability-standardization-decisions.md`
- **Deferred hardening:** `plan/death-claim/deferred-hardening.md`
- **Acceptance test boundary:** Canonical fixtures in `tests/acceptance/fixtures/death_claim/`

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- exact prompt capture or full external-model request logging
- review queue handoff
- evaluation recorder wiring
- policy lookup / retrieval context
- reviewability model changes
- exact confidence rubric changes
- a new telemetry backend, LangSmith rollout, OpenTelemetry rollout, or persistent trace storage
- broader guardrail or persistence work
- large custom visualization work beyond a lightweight static graph topology map

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `app/interface_adapters/orchestrators/nodes/generate_proceed_artifacts_node.py` - Branch-specific node for `proceed` artifact generation.
- `app/interface_adapters/orchestrators/nodes/generate_missing_info_artifacts_node.py` - Branch-specific node for `request_more_information` artifact generation.
- `app/interface_adapters/orchestrators/nodes/generate_hitl_artifacts_node.py` - Branch-specific node for `escalate_to_human_review` artifact generation.
- `drivers/ui/streamlit/widgets/graph_topology_panel.py` - Streamlit widget for lightweight in-app static graph topology mapping using Mermaid logic.

### Modified Files

- `app/interface_adapters/orchestrators/triage_graph_factory.py` - Replace the single monolithic artifact generation node with branch-specific generating nodes.
- `app/interface_adapters/orchestrators/triage_graph_state.py` - Expose `tokenized_document_facts` to the graph state as the dedicated security audit payload.
- `app/interface_adapters/orchestrators/nodes/tokenize_pii_node.py` - Populate `tokenized_document_facts` instead of overwriting `document_facts`.
- `app/interface_adapters/orchestrators/nodes/detokenize_pii_node.py` - Detokenize presentation outputs but do not overwrite `tokenized_document_facts`.
- `app/interface_adapters/orchestrators/nodes/generate_artifacts_node.py` - Retain as shared prompt/parsing helper logic or modify/deprecate as logic moves to specific nodes.
- `drivers/ui/streamlit/widgets/token_audit_panel.py` - Explicitly compare original/raw content vs `tokenized_document_facts` truthfully.
- `drivers/ui/streamlit/pages/1_triage_workbench.py` - Add `graph_topology_panel` to surface lightweight topology visualization.

## Assertions & Behavior Contracts

- Replace the single runtime branch sink `generate_artifacts` with three branch-specific nodes: `generate_proceed_artifacts`, `generate_missing_info_artifacts`, and `generate_hitl_artifacts`.
- Shared prompt/parsing helper logic may be kept in or extracted from `generate_artifacts_node.py`, but the runtime topology must no longer use one monolithic artifact-generation node.
- Add `tokenized_document_facts` to graph state as the dedicated audit payload.
- Keep `document_facts` available for internal deterministic logic (do not overwrite).
- All model-boundary artifact generation nodes must read from `tokenized_document_facts`.
- `detokenize_pii_node` must restore only user-facing output fields and must not overwrite `tokenized_document_facts`.
- The Streamlit security/audit panel must explicitly compare original/raw content or extracted facts with the tokenized model-boundary context.
- The audit UI must not claim “this is the exact prompt sent to OpenAI.”
- The graph topology panel should render the compiled static graph topology map in-app using the same Mermaid/PNG mechanism already demonstrated in `drivers/cli/commands/graph.py`.
- Any new branch-specific nodes and the new Streamlit graph panel must use the existing structured logging conventions (component + operation binding, `get_logger`, `log_exception`) rather than invent ad hoc logging.
- Logging must strictly prefer safe derived fields only (case id, disposition, generated field names, fact counts, tokenized-audit-ready flags, render success/failure) and never raw PII, full claim docs, raw prompts, model completions, or token maps.
- Observability is already standardized in the repo; this phase should only extend the existing patterns into the new nodes/widgets it introduces.

## Deferred Items Touched (If Any)

| Deferred item                                      | Current assumption used                                                                         | Hardening still required                                            |
|----------------------------------------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| Granular graph node tracing (1:1 Use Case Mapping) | Splitting `generate_artifacts` improves tracing resolution but is not yet a strict 1:1 mapping. | Full observability/tracing of every individual internal logic path. |
| LLM Fact Extraction + LLM Generation               | Tokenized audit snapshot increases PII boundary legibility without expanding extraction scope.  | Safely extracting explicit parameters with SLMs.                    |

## Ordered Implementation Steps

Implement in this order:

1. Update `TriageGraphState` to add `tokenized_document_facts`.
2. Modify `tokenize_pii_node.py` to populate `tokenized_document_facts` and preserve `document_facts`.
3. Modify `detokenize_pii_node.py` to ensure only downstream user-facing fields (summary, checklist, etc.) are detokenized, leaving `tokenized_document_facts` untouched.
4. Refactor `generate_artifacts_node.py` into shared helper logic and create `generate_proceed_artifacts_node.py`, `generate_missing_info_artifacts_node.py`, and `generate_hitl_artifacts_node.py`, ensuring each uses standard structured logging and reads from `tokenized_document_facts`.
5. Update `triage_graph_factory.py` topology to wire conditional routing edges into the new respective generation nodes, converging them on `detokenize_pii`.
6. Update `drivers/ui/streamlit/widgets/token_audit_panel.py` to truthfully compare raw facts against `tokenized_document_facts`.
7. Create `drivers/ui/streamlit/widgets/graph_topology_panel.py` applying the `draw_mermaid_png` rendering pattern with structured logging.
8. Update `drivers/ui/streamlit/pages/1_triage_workbench.py` to hook in the topology panel and adjust layout.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- **Graph routing after the branch split:** Verify that LangGraph runs on actual fixtures successfully trace through the independent node branches.
- **Preserved tokenized audit state:** Confirm `tokenized_document_facts` exists in the state without polluting `document_facts`.
- **Truthful Streamlit audit rendering:** Visually verify the Streamlit workbench displays clear, truthful original vs tokenized facts side-by-side in the audit panel without claiming exact prompt captures.
- **Graph topology rendering:** Visually verify the Streamlit workbench renders the topology Mermaid PNG map appropriately.
- **Adherence to current structured logging conventions for new code:** Verify terminal logs use correct `log.bind(node=...)`, `log.info("started")`, etc., for all newly created files and that no raw PII data leaked to standard output.

## Assumptions

- The current workbench is structurally close to the desired demo, but the current audit panel is not truthful because it labels raw content as scrubbed.
- Treat the node split and the truthful audit snapshot as the core of the phase.
- Use the static graph topology panel as a lightweight visual aid mapping what happened, not as a deep primary traceability mechanism or developer debugger trace viewer.
- The latest observability commit already standardized structured logging across the active triage surfaces; this phase should only extend that pattern to the new nodes/widget it introduces.
