# Death-Claim Tree A Code Map

> **Purpose:** Show how the selected Tree A / CA-preserving steel-thread shape can map the death-claim triage scenario into a concrete PoC code layout.

---

**Status:** Active PoC planning companion

This document is a **PoC planning companion** for the selected Tree A shape. It shows how the death-claim triage scenario from [`death-claim-workshop-spec.md`](./death-claim-workshop-spec.md) could map into a CA-preserving structure without turning the workshop contract itself into implementation detail.

**Deferred hardening register:** [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md)

- The exact missing-vs-ambiguous boundary is a provisional assumption.
- The exact tone rubric for claimant-facing follow-up is a provisional assumption.
- The exact governance/data-science review scorecard is a provisional assumption.
- The exact confidence/reviewability model is a provisional assumption.

## The Two Layering Systems

Tree A keeps the existing Lean-Clean CA structure:

1. `drivers/`
2. `app/interface_adapters/orchestrators/`
3. `app/use_cases/`
4. `app/adapters/`
5. `app/infrastructure/`

The five engineering layers still sit *inside* that structure:

1. Prompt Routing
2. Retrieval Augmented Generation (RAG)
3. Prompt Engineering
4. Autonomous Agents
5. Operational Infrastructure

For this scenario, those engineering layers mean:

- **Prompt Routing:** deciding which bounded triage path the intake bundle should take
- **RAG:** assembling policy, document, and beneficiary context into grounded model-facing inputs
- **Prompt Engineering:** generating summary, checklist, follow-up, and rationale artifacts
- **Autonomous Agents:** bounded orchestration across normalization, analysis, branching, and handoff
- **Operational Infrastructure:** PII boundaries, auditability, review-queue handoff, evals, and retention

## Provisional Assumptions From The Defer Register

These assumptions are sufficient for a first downstream translation, but they are not yet hardened PoC design guidance.

| Area                       | Provisional assumption                                                                                                                                                                                                                                                                              |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Missing vs ambiguous       | Treat `missing information` as a straightforward gap in required intake artifacts or fields. Treat `ambiguous / HITL` as conflicting, uncertain, or materially review-sensitive context. Exact threshold is deferred in [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md). |
| Follow-up tone             | Follow-up language should be empathetic, operationally appropriate, and explicitly non-adjudicative. Exact tone rubric is deferred in [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md).                                                                                   |
| Review metrics             | The system should preserve inspectability, auditability, and disposition traceability. Exact governance/data-science scorecard is deferred in [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md).                                                                           |
| Confidence / reviewability | Use `High / Medium / Low` confidence bands plus explicit `reviewability_flags` and `escalation_reasons`. Exact rubric is deferred in [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md).                                                                                    |

---

## 5x5 Crosswalk: Engineering Layers vs CA Layers

| Engineering Layer              | Drivers                                                                                                                                                                                      | Orchestrators                                                                                                                           | Use Cases                                                                                                                                                                                                                                                                               | Adapters                                                                                                                                                          | Infrastructure                                                                                                                                                          |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Prompt Routing**             | Receive intake requests, validate shape, and capture operator/workbench metadata. Example: `drivers/api/schemas/death_claim_request.py`, `drivers/ui/streamlit/pages/1_triage_workbench.py`. | Decide whether the bundle is ready to proceed, needs more information, or must escalate. Example: `death_claim_triage_orchestrator.py`. | Normalize the bundle, assess completeness, detect ambiguity, assess reviewability, and choose the bounded disposition. Example: `normalize_claim_bundle_uc.py`, `assess_completeness_uc.py`, `detect_ambiguity_uc.py`, `assess_reviewability_uc.py`, `decide_triage_disposition_uc.py`. | Hold policy-lookup, document-intake, and triage-model boundaries. Example: `app/adapters/policy_lookup/`, `app/adapters/document_intake/`, `app/adapters/model/`. | Persist disposition history and route telemetry for later review. Example: `app/infrastructure/repositories/triage_runs/`, `app/infrastructure/telemetry/metrics.py`.   |
| **RAG**                        | Expose intake documents, policy references, and citations through workbench/API views.                                                                                                       | Coordinate policy/admin/document retrieval as one stage in the broader triage flow.                                                     | Assemble grounded context for summary, checklist, and rationale generation. Example: `verify_policy_context_uc.py`, `extract_document_facts_uc.py`, `assemble_model_context_uc.py`.                                                                                                     | Connect to policy admin lookup, document storage, and citation formatting. Example: `policy_lookup_adapter.py`, `document_intake_adapter.py`.                     | Store source documents, retrieved facts, and trace records. Example: `app/infrastructure/repositories/intake_bundles/`, `app/infrastructure/telemetry/trace_logger.py`. |
| **Prompt Engineering**         | Accept UI/API inputs that shape artifact delivery, such as channel or review mode.                                                                                                           | Decide which artifact-generation flow to run for the chosen disposition.                                                                | Generate `CASE_SUMMARY`, `REQUIREMENTS_CHECKLIST`, `FOLLOW_UP_MESSAGE`, `ROUTING_DECISION`, or `HITL_REVIEW_TASK`.                                                                                                                                                                      | Own prompt templates, output parsers, and no-adjudication policy checks. Example: `app/adapters/model/prompts/`, `app/adapters/safety/`.                          | Store prompt usage traces and artifact-generation telemetry. Example: `app/infrastructure/telemetry/`, `app/infrastructure/cost/usage_rollups.py`.                      |
| **Autonomous Agents**          | Expose run, replay, and review entry points via workbench UI, API, CLI, worker, and MCP.                                                                                                     | Coordinate bounded multi-step orchestration across normalization, privacy boundary, generation, validation, and handoff.                | Plan the triage flow, generate artifacts, and create review tasks where needed. Example: `create_hitl_review_task_uc.py`, `generate_follow_up_message_uc.py`.                                                                                                                           | Connect to model, privacy, review-queue, and event boundaries. Example: `app/adapters/model/`, `app/adapters/safety/`, `app/adapters/review_queue/`.              | Provide queues, repositories, checkpoints, and background processing. Example: `app/infrastructure/queues/`, `app/infrastructure/checkpoints/`.                         |
| **Operational Infrastructure** | Expose health, review, audit, and eval screens/endpoints.                                                                                                                                    | Trigger evaluation, review, and replay flows.                                                                                           | Enforce PII tokenization boundaries, validate generated artifacts, record audit events, and emit reviewable traces. Example: `tokenize_pii_for_model_uc.py`, `validate_follow_up_output_uc.py`, `validate_routing_rationale_uc.py`, `evaluate_triage_run_uc.py`.                        | Implement PII guardrails, message policies, audit sinks, review queues, and evaluation adapters.                                                                  | Persist traces, audits, review items, metrics, and retention jobs. Example: `app/infrastructure/repositories/reviews/`, `app/infrastructure/retention/`.                |

---

## Full Tree A File Tree

```text
bestow-poc/
├─ README.md
├─ Makefile
├─ .gitignore
├─ .dockerignore
├─ .env.example
├─ pyproject.toml
│
├─ app/
│  ├─ entities/
│  │  ├─ claim_intake_bundle.py
│  │  ├─ policy_context.py
│  │  ├─ document_facts.py
│  │  ├─ pii_token_map.py
│  │  ├─ completeness_assessment.py
│  │  ├─ ambiguity_assessment.py
│  │  ├─ reviewability_assessment.py
│  │  ├─ triage_disposition.py
│  │  ├─ confidence_band.py
│  │  ├─ case_summary.py
│  │  ├─ requirements_checklist.py
│  │  ├─ follow_up_request.py
│  │  ├─ routing_decision.py
│  │  ├─ hitl_review_task.py
│  │  ├─ review_queue_item.py
│  │  ├─ trace_event.py
│  │  ├─ audit_record.py
│  │  ├─ retention_policy.py
│  │  ├─ errors.py
│  │  └─ value_objects.py
│  │
│  ├─ use_cases/
│  │  ├─ normalize_claim_bundle_uc.py
│  │  ├─ verify_policy_context_uc.py
│  │  ├─ extract_document_facts_uc.py
│  │  ├─ tokenize_pii_for_model_uc.py
│  │  ├─ assemble_model_context_uc.py
│  │  ├─ assess_completeness_uc.py
│  │  ├─ detect_ambiguity_uc.py
│  │  ├─ assess_reviewability_uc.py
│  │  ├─ decide_triage_disposition_uc.py
│  │  ├─ generate_case_summary_uc.py
│  │  ├─ generate_requirements_checklist_uc.py
│  │  ├─ generate_follow_up_message_uc.py
│  │  ├─ generate_routing_decision_uc.py
│  │  ├─ create_hitl_review_task_uc.py
│  │  ├─ validate_follow_up_output_uc.py
│  │  ├─ validate_routing_rationale_uc.py
│  │  ├─ emit_trace_event_uc.py
│  │  ├─ record_audit_event_uc.py
│  │  ├─ evaluate_triage_run_uc.py
│  │  └─ apply_retention_policy_uc.py
│  │
│  ├─ interface_adapters/
│  │  ├─ orchestrators/
│  │  │  ├─ death_claim_triage_orchestrator.py
│  │  │  ├─ validation_orchestrator.py
│  │  │  ├─ review_orchestrator.py
│  │  │  └─ evaluation_orchestrator.py
│  │  ├─ presenters/
│  │  │  ├─ triage_result_presenter.py
│  │  │  ├─ review_queue_presenter.py
│  │  │  ├─ trace_presenter.py
│  │  │  └─ eval_report_presenter.py
│  │  └─ mappers/
│  │     ├─ workbench_request_mapper.py
│  │     ├─ api_request_mapper.py
│  │     ├─ worker_job_mapper.py
│  │     └─ response_mapper.py
│  │
│  ├─ adapters/
│  │  ├─ policy_lookup/
│  │  │  ├─ protocol.py
│  │  │  ├─ fake.py
│  │  │  └─ policy_lookup_adapter.py
│  │  ├─ document_intake/
│  │  │  ├─ protocol.py
│  │  │  ├─ fake.py
│  │  │  ├─ document_intake_adapter.py
│  │  │  ├─ death_certificate_parser.py
│  │  │  └─ beneficiary_record_parser.py
│  │  ├─ model/
│  │  │  ├─ protocol.py
│  │  │  ├─ fake.py
│  │  │  ├─ prompts/
│  │  │  │  ├─ case_summary_prompt_template.py
│  │  │  │  ├─ requirements_checklist_prompt_template.py
│  │  │  │  ├─ follow_up_message_prompt_template.py
│  │  │  │  └─ routing_rationale_prompt_template.py
│  │  │  ├─ parsers/
│  │  │  │  ├─ case_summary_parser.py
│  │  │  │  ├─ checklist_parser.py
│  │  │  │  ├─ follow_up_message_parser.py
│  │  │  │  └─ routing_rationale_parser.py
│  │  │  └─ providers/
│  │  │     ├─ openai_adapter.py
│  │  │     └─ anthropic_adapter.py
│  │  ├─ safety/
│  │  │  ├─ protocol.py
│  │  │  ├─ fake.py
│  │  │  ├─ pii_guardrail_adapter.py
│  │  │  ├─ token_mapper.py
│  │  │  ├─ claimant_message_policy.py
│  │  │  ├─ routing_rationale_policy.py
│  │  │  ├─ reviewability_policy.py
│  │  │  ├─ no_adjudication_validator.py
│  │  │  └─ audit.py
│  │  ├─ review_queue/
│  │  │  ├─ protocol.py
│  │  │  ├─ fake.py
│  │  │  └─ review_queue_adapter.py
│  │  ├─ events/
│  │  │  ├─ protocol.py
│  │  │  ├─ fake.py
│  │  │  ├─ telemetry_sink.py
│  │  │  └─ audit_sink.py
│  │  └─ evals/
│  │     ├─ protocol.py
│  │     ├─ fake.py
│  │     └─ triage_eval_adapter.py
│  │
│  └─ infrastructure/
│     ├─ queues/
│     │  ├─ protocol.py
│     │  ├─ in_memory.py
│     │  ├─ redis_queue.py
│     │  └─ review_queue.py
│     ├─ checkpoints/
│     │  ├─ protocol.py
│     │  ├─ in_memory.py
│     │  └─ postgres_checkpoint_store.py
│     ├─ repositories/
│     │  ├─ intake_bundles/
│     │  │  ├─ protocol.py
│     │  │  ├─ in_memory.py
│     │  │  └─ postgres.py
│     │  ├─ triage_runs/
│     │  │  ├─ protocol.py
│     │  │  ├─ in_memory.py
│     │  │  └─ postgres.py
│     │  ├─ reviews/
│     │  │  ├─ protocol.py
│     │  │  ├─ in_memory.py
│     │  │  └─ postgres.py
│     │  ├─ evals/
│     │  │  ├─ protocol.py
│     │  │  ├─ in_memory.py
│     │  │  └─ postgres.py
│     │  └─ audit/
│     │     ├─ protocol.py
│     │     ├─ in_memory.py
│     │     └─ postgres.py
│     ├─ telemetry/
│     │  ├─ trace_logger.py
│     │  ├─ metrics.py
│     │  ├─ otel.py
│     │  └─ dashboards.py
│     ├─ cost/
│     │  ├─ token_meter.py
│     │  ├─ budget_ledger.py
│     │  └─ usage_rollups.py
│     ├─ security/
│     │  ├─ secret_loader.py
│     │  ├─ kms.py
│     │  └─ network_policy.py
│     ├─ retention/
│     │  ├─ retention_jobs.py
│     │  └─ purge_triage_runs.py
│     └─ orm_models/
│        ├─ intake_bundle_orm.py
│        ├─ triage_run_orm.py
│        ├─ review_case_orm.py
│        └─ eval_result_orm.py
│
├─ drivers/
│  ├─ api/
│  │  ├─ main.py
│  │  ├─ routes/
│  │  │  ├─ triage.py
│  │  │  ├─ reviews.py
│  │  │  └─ health.py
│  │  ├─ schemas/
│  │  │  ├─ death_claim_request.py
│  │  │  ├─ death_claim_response.py
│  │  │  └─ review_decision_request.py
│  │  └─ dependencies.py
│  ├─ orchestrator/
│  │  ├─ main.py
│  │  ├─ run_once.py
│  │  ├─ schedule.py
│  │  └─ dependencies.py
│  ├─ worker/
│  │  ├─ worker.py
│  │  ├─ tasks/
│  │  │  ├─ process_triage_run.py
│  │  │  ├─ enqueue_review_task.py
│  │  │  ├─ run_eval_suite.py
│  │  │  └─ apply_retention_jobs.py
│  │  └─ dependencies.py
│  ├─ mcp/
│  │  ├─ main.py
│  │  ├─ tools/
│  │  │  ├─ lookup_policy_context.py
│  │  │  ├─ inspect_review_case.py
│  │  │  └─ replay_triage_trace.py
│  │  └─ dependencies.py
│  ├─ cli/
│  │  ├─ __main__.py
│  │  ├─ commands/
│  │  │  ├─ triage_case.py
│  │  │  ├─ replay_trace.py
│  │  │  └─ inspect_review_queue.py
│  │  └─ dependencies.py
│  └─ ui/
│     └─ streamlit/
│        ├─ app.py
│        ├─ pages/
│        │  ├─ 1_triage_workbench.py
│        │  ├─ 2_case_trace.py
│        │  ├─ 3_review_queue.py
│        │  └─ 4_eval_dashboard.py
│        ├─ widgets/
│        │  ├─ bundle_viewer.py
│        │  ├─ disposition_panel.py
│        │  └─ token_audit_panel.py
│        └─ dependencies.py
│
├─ contracts/
│  ├─ api/
│  │  ├─ death_claim_request.py
│  │  ├─ death_claim_response.py
│  │  └─ review_case_response.py
│  ├─ jobs/
│  │  ├─ triage_run_job.py
│  │  ├─ review_queue_job.py
│  │  └─ retention_job.py
│  └─ events/
│     ├─ triage_started.py
│     ├─ triage_completed.py
│     ├─ human_review_requested.py
│     └─ policy_boundary_violation.py
│
├─ eval/
│  ├─ datasets/
│  ├─ rubrics/
│  └─ golden_cases/
│
├─ deploy/
│  ├─ local/
│  │  ├─ docker-compose.yaml
│  │  └─ .env.local.example
│  ├─ kubernetes/
│  │  ├─ api.yaml
│  │  ├─ worker.yaml
│  │  └─ review-queue.yaml
│  └─ runbooks/
│     ├─ triage-workbench.md
│     ├─ human-review.md
│     └─ retention.md
│
├─ tests/
│  ├─ acceptance/
│  ├─ unit/
│  ├─ integration/
│  ├─ contract/
│  └─ smoke/
│
└─ docs/
   ├─ death-claim-workflow.md
   ├─ pii-boundary.md
   └─ review-queue-handoff.md
```

---

## Where The Logic Lives By CA Layer

### `drivers/`

This layer owns entrypoints, request parsing, transport validation, and delivery surfaces for the internal workbench, API, CLI, worker, and MCP entrypoints.

Examples:

- `drivers/ui/streamlit/pages/1_triage_workbench.py`
- `drivers/api/routes/triage.py`
- `drivers/worker/tasks/process_triage_run.py`
- `drivers/cli/commands/triage_case.py`

What lives here:

- request and response schemas
- channel-specific auth/session details
- operator-facing workbench controls
- delivery-specific dependency wiring

What does not live here:

- completeness logic
- ambiguity logic
- policy-lookup rules
- no-adjudication enforcement

### `app/interface_adapters/orchestrators/`

This layer sequences the use cases into a bounded death-claim triage flow.

Examples:

- `death_claim_triage_orchestrator.py`
- `validation_orchestrator.py`
- `review_orchestrator.py`

What lives here:

- step ordering
- branching between `proceed`, `request_more_information`, and `escalate_to_human_review`
- combining rule outcomes into a visible reviewability/confidence signal
- handoff between interactive and async paths
- coordination between privacy boundary, generation, validation, and review queue

What does not live here:

- raw vendor API code
- persistence implementations
- presenter formatting

### `app/use_cases/`

This is where most of the scenario-specific application logic lives.

Examples:

- normalization: `normalize_claim_bundle_uc.py`
- context assembly: `verify_policy_context_uc.py`, `extract_document_facts_uc.py`, `assemble_model_context_uc.py`
- privacy boundary: `tokenize_pii_for_model_uc.py`
- triage logic: `assess_completeness_uc.py`, `detect_ambiguity_uc.py`, `decide_triage_disposition_uc.py`
- reviewability logic: `assess_reviewability_uc.py`
- artifact generation: `generate_case_summary_uc.py`, `generate_requirements_checklist_uc.py`, `generate_follow_up_message_uc.py`, `generate_routing_decision_uc.py`, `create_hitl_review_task_uc.py`
- validation and ops: `validate_follow_up_output_uc.py`, `validate_routing_rationale_uc.py`, `record_audit_event_uc.py`, `evaluate_triage_run_uc.py`

### `app/adapters/`

This layer owns the external boundaries and specialized policy logic.

Examples:

- `app/adapters/policy_lookup/policy_lookup_adapter.py`
- `app/adapters/document_intake/document_intake_adapter.py`
- `app/adapters/safety/pii_guardrail_adapter.py`
- `app/adapters/safety/no_adjudication_validator.py`
- `app/adapters/safety/reviewability_policy.py`
- `app/adapters/review_queue/review_queue_adapter.py`

This is also where prompt templates, parsers, and policy guards should live for generated artifacts.

### `app/infrastructure/`

This layer owns queues, repositories, checkpoints, telemetry, budgets, retention, and other operational mechanics.

Examples:

- `app/infrastructure/repositories/triage_runs/postgres.py`
- `app/infrastructure/repositories/reviews/postgres.py`
- `app/infrastructure/telemetry/otel.py`
- `app/infrastructure/retention/purge_triage_runs.py`

---

## Guardrails Ownership In Tree A

Guardrails should remain split into four distinct concerns.

| Concern                            | Primary owner                     | Example files                                                                                                                                                      | Notes                                                                                               |
|------------------------------------|-----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| **Transport validation**           | Drivers + mappers                 | `drivers/api/schemas/death_claim_request.py`, `app/interface_adapters/mappers/api_request_mapper.py`                                                               | Request-shape and boundary validation only.                                                         |
| **Pre-model privacy boundary**     | Use cases calling safety adapters | `tokenize_pii_for_model_uc.py`, `app/adapters/safety/pii_guardrail_adapter.py`, `token_mapper.py`                                                                  | Raw demographics and other PII must not cross the external model boundary.                          |
| **Post-model artifact validation** | Use cases calling safety adapters | `validate_follow_up_output_uc.py`, `validate_routing_rationale_uc.py`, `claimant_message_policy.py`, `routing_rationale_policy.py`, `no_adjudication_validator.py` | Follow-up and rationale artifacts are checked before release or queue handoff.                      |
| **Presentation shaping**           | Presenters                        | `triage_result_presenter.py`, `review_queue_presenter.py`                                                                                                          | Presenters format the result and remove internal-only details. They do not own the policy decision. |

### Pre-model guardrails

Pre-model guardrails are where the PII rule from the workshop spec becomes concrete:

- intake bundle may contain claimant demographics and other raw PII
- model-facing context is tokenized or pseudonymized before external analysis
- referential meaning is preserved through stable safe tokens

This is a core scenario requirement, not an optional enhancement.

### Post-model guardrails

Post-model validation is where the artifact itself is checked:

- claimant-facing follow-up must remain empathetic and operationally appropriate
- rationale must remain non-adjudicative
- routing explanation must stay bounded to triage and next-step orchestration

The exact tone rubric is a **provisional assumption from [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md)**.

### Missing-vs-ambiguous branching

The branching logic belongs in use cases and orchestrators, not in presenters.

High-level provisional rule:

- `missing information` means the bundle is incomplete in a way that can be requested directly
- `ambiguous / HITL` means the bundle has unresolved uncertainty, conflicting context, or material review sensitivity

The exact threshold is a **provisional assumption from [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md)**.

### Confidence / reviewability

Tree A should not rely on a raw numeric score as the first-class gate for this scenario.

Instead:

- explicit findings and reasons remain the primary gate
- a `High / Medium / Low` `confidence_band` summarizes reviewability
- `reviewability_flags` and `escalation_reasons` remain visible for operators and reviewers

Example ownership:

- `assess_reviewability_uc.py`
- `reviewability_assessment.py`
- `confidence_band.py`
- `app/adapters/safety/reviewability_policy.py`

High-level provisional rule:

- `High` means bounded and ready to proceed
- `Medium` means bounded but still requires a follow-up loop
- `Low` means the case should escalate to human review

The exact rubric is a **provisional assumption from [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md)**.

---

## Where Each Scenario Concern Shows Up In The Tree

### Intake normalization

Primary files:

- `normalize_claim_bundle_uc.py`
- `workbench_request_mapper.py`
- `api_request_mapper.py`

### Policy lookup and document context assembly

Primary files:

- `verify_policy_context_uc.py`
- `extract_document_facts_uc.py`
- `app/adapters/policy_lookup/`
- `app/adapters/document_intake/`

### PII tokenization before external analysis

Primary files:

- `tokenize_pii_for_model_uc.py`
- `app/adapters/safety/pii_guardrail_adapter.py`
- `token_mapper.py`

### Completeness and ambiguity assessment

Primary files:

- `assess_completeness_uc.py`
- `detect_ambiguity_uc.py`
- `decide_triage_disposition_uc.py`

### Confidence / reviewability assessment

Primary files:

- `assess_reviewability_uc.py`
- `reviewability_assessment.py`
- `confidence_band.py`
- `app/adapters/safety/reviewability_policy.py`

### Claimant-facing follow-up generation

Primary files:

- `generate_requirements_checklist_uc.py`
- `generate_follow_up_message_uc.py`
- `app/adapters/model/prompts/follow_up_message_prompt_template.py`
- `app/adapters/safety/claimant_message_policy.py`

### HITL review task generation

Primary files:

- `create_hitl_review_task_uc.py`
- `app/adapters/review_queue/review_queue_adapter.py`
- `review_orchestrator.py`

### Audit, eval, and review-queue handoff

Primary files:

- `generate_routing_decision_uc.py`
- `record_audit_event_uc.py`
- `evaluate_triage_run_uc.py`
- `app/adapters/events/`
- `app/adapters/evals/`
- `app/infrastructure/repositories/reviews/`

The exact review/demo scorecard remains a **provisional assumption from [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md)**.

The exact reviewability rubric also remains a **provisional assumption from [`death-claim-deferred-hardening.md`](./death-claim-deferred-hardening.md)**.

---

## Reading Tree A Correctly For This Scenario

If Tree A is used for the death-claim triage scenario, the right mental model is:

- the **workshop spec** defines the stakeholder contract
- the **defer register** marks the known hardening gaps
- the **orchestrators and use cases** carry most of the triage behavior
- the **adapters** carry policy lookup, document intake, model, privacy, queue, and evaluation boundaries
- the **infrastructure** carries traceability, persistence, queueing, and retention
- the **presenters** format already-bounded results without taking over policy decisions
- the **confidence/reviewability signal** is band-plus-reasons, not a raw numeric score

That is the Tree A claim this companion is trying to make visible.
