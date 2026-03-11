# Death Claim Triage: Phase 6 Implementation Plan (Delivery Surfaces)

## Phase Summary

- **Scenario:** Death Claim Triage (Tree A)
- **Phase Goal:** Connect the complete LangGraph workflow to the delivery surfaces: a Streamlit internal workbench for the demo, and a thin FastAPI shell. Visually prove the PII privacy boundary.
- **Status:** ready

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **Architecture decisions:** `plan/decisions/_langgraph-architecture-decisions.md`
- **Deferred hardening:** `plan/death-claim/deferred-hardening.md`
- **Acceptance test boundary:** `tests/acceptance/features/test_death_claim_intake_triage.py`

## Out Of Scope

- Over-engineered mappers and presenters (`workbench_request_mapper.py`, `triage_result_presenter.py`). Streamlit and FastAPI will interact with the LangGraph state dict directly to save time and reduce boilerplate.
- Persistent databases or complex queue workers.

## Target Production Surface

### New Files

- `drivers/ui/streamlit/pages/1_triage_workbench.py` - The primary demo UI page.
- `drivers/ui/streamlit/widgets/bundle_viewer.py` - Panel displaying the original intake input.
- `drivers/ui/streamlit/widgets/disposition_panel.py` - Panel displaying the LLM-generated artifacts (including the new `hitl_review_task`), routing decision, and confidence band.
- `drivers/ui/streamlit/widgets/token_audit_panel.py` - A crucial visual audit panel proving that PII was scrubbed *before* hitting the LLM.
- `drivers/api/routes/health.py`
- `drivers/api/routes/triage.py`
- `drivers/api/schemas/death_claim_request.py`
- `drivers/api/schemas/death_claim_response.py` (ensure to include the new `hitl_review_task` field)

### Modified Files

- `drivers/ui/streamlit/app.py` - Ensure navigation coordinates to the new workbench.
- `drivers/api/main.py` - Register the new FastAPI routers.

## Assertions & Behavior Contracts

- The UI must clearly contrast the 3 representative cases (Complete, Missing Info, Ambiguous).
- The `token_audit_panel` MUST make the privacy tokenization obvious to the audience, fulfilling the core security requirement of the workshop spec.
- Both Streamlit and FastAPI must execute the EXACT same compiled `TriageGraph` instance. Fast integration, single source of truth.

## Deferred Items Touched (If Any)

| Deferred item      | Current assumption used                          | Hardening still required      |
|--------------------|--------------------------------------------------|-------------------------------|
| Secrets Management | Using `.env` injection for quick local iteration | Cloud secrets manager mapping |

## Ordered Implementation Steps

Implement in this order:

1. Build the FastAPI schemas and routes (`health` and `triage`) to expose the graph as an API.
2. Update `drivers/api/main.py` to mount the routes.
3. Build the Streamlit widgets (`bundle_viewer`, `disposition_panel`, `token_audit_panel`).
4. Assemble `1_triage_workbench.py` with the 3 canonical fixtures available as easy "demo load" buttons.
5. Manually test the Streamlit UI to ensure the layout makes the architectural decisions (explicit routing, human-in-the-loop, PII tokenization) highly visible for the 5-minute recording.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- `streamlit run drivers/ui/streamlit/app.py` loads the workbench successfully and the 3 fixtures exercise the full end-to-end LangGraph triage flow with LLM outputs and privacy tokenization displayed.

## Assumptions

- Streamlit will directly consume and format the `TriageGraphState` returned by the graph rather than requiring a secondary Presentation mapper.
