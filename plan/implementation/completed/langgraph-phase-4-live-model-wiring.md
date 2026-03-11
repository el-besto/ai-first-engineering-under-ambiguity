# Death Claim Triage: Phase 4 Implementation Plan (Live Model & Wiring)

## Phase Summary

- **Scenario:** Death Claim Triage (Tree A)
- **Phase Goal:** Swap to a live LLM adapter, ensure Streamlit and FastAPI hit the same graph interface, and validate the 3 canonical cases end-to-end.
- **Status:** awaiting_review

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **PLAN_HUMAN_FINAL:** `.scratch/PLAN_HUMAN_FINAL.md` (Block 5/6 - Connect Surfaces to the Graph)
- **Acceptance Boundary:** `tests/acceptance/` and `drivers/ui/streamlit`

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- Re-architecting deterministic rules or extraction facts (completed in Phase 2/3).
- Scaling synthetic data or broader evaluation pipelines.

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `app/adapters/model/live_chat_model_adapter.py` - Generic provider-backed adapter implementing `model/protocol.py` (wrapping LangChain's `init_chat_model`).

### Modified Files

- `drivers/api/dependencies.py` - Inject live adapters using `.env` logic.
- `drivers/ui/streamlit/dependencies.py` - Wire graph instantiation to Streamlit session state.
- `tests/acceptance/test_workflow_facade.py` - Validate acceptance metrics using the live configuration across all 3 representative cases.

## Assertions & Behavior Contracts

- Both UI and API MUST invoke the exact same `TriageGraphFactory.build_triage_graph()` instance.
- Live model configuration must be opted-in via `.env`, defaulting to fake-backed if credentials are missing to protect CI pipelines.
- **Security Check**: When configuring `LLM_MAIN_MODEL` and API Keys in `APIConfig`/`UIConfig`, ensure keys are defined using Pydantic's `Field(..., repr=False)` to prevent accidental logging or exposure of the token in trace outputs.
- The model adapter MUST be generically configurable (accepting `model_name`, `api_base`, `api_key`) to seamlessly support later injection of a local SLM (via Ollama/vLLM) for the DSPy PII redaction stretch goal without needing to author a new adapter class.
- Acceptance fixtures must complete end-to-end dynamically producing meaningful `CASE_SUMMARY`, `REQUIREMENTS_CHECKLIST`, `FOLLOW_UP_MESSAGE`, and `HITL_REVIEW_TASK`.

## Deferred Items Touched (If Any)

| Deferred item                      | Current assumption used                                             | Hardening still required     |
|------------------------------------|---------------------------------------------------------------------|------------------------------|
| Fake System Collaborator Adapters  | Intake, Policy, and Queue remain mock-backed.                       | Live enterprise integration. |
| Synthetic Data Pipeline Generation | We test exclusively against the 3 canonical hand-authored fixtures. | Broader evaluation matrices. |

## Ordered Implementation Steps

Implement in this order:

1. Build `live_chat_model_adapter.py` using LangChain's generic `init_chat_model`.
2. Update `.env.example` and `config` models to enforce explicit domain vars (`LLM_MAIN_MODEL`, `LLM_MAIN_API_KEY`, etc.).
3. Construct the provider injection swap in `drivers/api/dependencies.py`. Ensure the `APIConfig` is used to map explicit vars to the model adapter endpoints.
4. Construct the same provider injection swap in `drivers/ui/streamlit/dependencies.py` injecting `UIConfig`.
5. Wrap `TriageGraphState` back into the final `TriageResult` at the driver boundary API mapping edge.
6. Create Live-Model Acceptance Tests ensuring all 3 case bounds pass.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- `docker compose up` or `tilt up` locally mounts Streamlit and FastAPI successfully.
- Submitting the 3 known fixtures directly inside Streamlit yields the 3 separate, correct deterministic branch dispositions.
- Live LLM artifacts are generated securely without leaking physical PII (verified via LangSmith/Studio trace inspection if enabled locally).

## Assumptions

- We will utilize explicit domain variables (`LLM_*`) to maintain strict routing control between main logic and future guardrail nodes.
- The `PIIGuardrailAdapter` will remain in place, and this generic adapter sets the stage for injecting a local SLM specifically into that guardrail node as a stretch goal.
- We rely strictly on the 3 canonical text fixtures to prevent scope bloat.
