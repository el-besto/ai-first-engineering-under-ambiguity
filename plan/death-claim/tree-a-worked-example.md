# Death-Claim Tree A Worked Example

> **Purpose:** Show the selected Tree A shape in motion using the death-claim triage scenario so the CA layers and engineering layers can be read together during PoC planning.

---

**Status:** Active PoC planning companion

This document is a **post-workshop, downstream walkthrough**. It derives from:

- [`workshop-spec.md`](./workshop-spec.md)
- [`deferred-hardening.md`](./deferred-hardening.md)

It is not the place where the stakeholder contract is created. It is the place where the current workshop scenario is translated into a Tree A vertical-slice example.

**Deferred hardening register:** [`deferred-hardening.md`](./deferred-hardening.md)

- Any missing-vs-ambiguous thresholds, claimant-tone specifics, or governance/data-science scorecard items that are not pinned down here should be read as intentional provisional assumptions from the defer register.
- The exact confidence/reviewability rubric is also an intentional provisional assumption from the defer register.

**Current build target note:** The current implementation target is the minimal steel thread in [`tree-a-code-map.md`](./tree-a-code-map.md): Streamlit as the primary demo UI, a thin FastAPI ingress, a LangGraph-owned triage flow, `deploy/local/compose.yaml`, and fixture-driven tests. Some later sections in this walkthrough still illustrate broader Tree A expansion paths beyond the current slice.

## Business Scenario

A claims operations specialist loads a death-claim intake bundle into an internal workbench.

The bundle may include:

- claimant request details
- policy summary context
- intake form details
- death certificate
- beneficiary record

The system must:

1. normalize the bundle
2. assemble policy and document context
3. tokenize claimant demographics and other PII before any external model-facing analysis
4. assess completeness and ambiguity
5. assess reviewability / confidence band
6. choose one bounded disposition using reasons + band:
   - proceed
   - request more information
   - escalate to human review
7. generate the corresponding operational artifacts
8. keep no-adjudication and review-boundary constraints explicit

## Representative Cases

### Case A: Complete Intake

Expected outputs:

- `CASE_SUMMARY`
- `ROUTING_DECISION`
- `confidence_band = High`

### Case B: Missing Information

Expected outputs:

- `REQUIREMENTS_CHECKLIST`
- `FOLLOW_UP_MESSAGE`
- `confidence_band = Medium`
- `reviewability_flags`

### Case C: Ambiguous / HITL

Expected outputs:

- `HITL_REVIEW_TASK`
- `confidence_band = Low`
- `escalation_reasons`
- escalation rationale

---

## End-To-End Flow

| Step | What happens                                                                                            | Primary CA owner                        | Main files                                                                                                        |
|------|---------------------------------------------------------------------------------------------------------|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 1    | Intake workbench or thin API receives the claim bundle and forwards it into the graph-owned triage path | Drivers + mappers + orchestrators       | `drivers/ui/streamlit/pages/1_triage_workbench.py`, `drivers/api/routes/triage.py`, `death_claim_triage_graph.py` |
| 2    | Policy/admin/document context is assembled                                                              | Orchestrator + use cases + adapters     | `death_claim_triage_orchestrator.py`, `verify_policy_context_uc.py`, `extract_document_facts_uc.py`               |
| 3    | PII is tokenized before external model-facing analysis                                                  | Use cases + safety adapters             | `tokenize_pii_for_model_uc.py`, `pii_guardrail_adapter.py`                                                        |
| 4    | Completeness and ambiguity are assessed                                                                 | Use cases                               | `assess_completeness_uc.py`, `detect_ambiguity_uc.py`                                                             |
| 5    | Reviewability is assessed and summarized as a confidence band plus reasons                              | Use cases + safety policy               | `assess_reviewability_uc.py`, `reviewability_policy.py`                                                           |
| 6    | One bounded disposition is chosen using reasons + band                                                  | Use cases                               | `decide_triage_disposition_uc.py`                                                                                 |
| 7    | Disposition-specific artifacts are generated                                                            | Use cases + model/safety adapters       | `generate_case_summary_uc.py`, `generate_follow_up_message_uc.py`, `create_hitl_review_task_uc.py`                |
| 8    | Results are validated, presented, and routed onward                                                     | Use cases + presenters + infrastructure | `validate_follow_up_output_uc.py`, `triage_result_presenter.py`, `review_queue_adapter.py`                        |

For the current minimal steel thread, the primary build target is the workbench-plus-API ingress over the graph-owned triage path. Any later validation, review, or background-processing references in this walkthrough should be read as broader Tree A expansion examples unless they are explicitly called out as part of the current slice.

---

## Step 1: Intake Workbench Or Thin API Receives The Claim Bundle

### What happens

The internal workbench is the primary surface for this scenario. A claims operations specialist selects or uploads a representative intake bundle and asks the system to triage it. The same graph-owned path can also be reached through a thin internal API for programmatic invocation and faster test cycles.

### CA owner

- `drivers/ui/`
- `drivers/api/`
- `app/interface_adapters/mappers/`
- `app/interface_adapters/orchestrators/`

### Tree A files involved

- `drivers/ui/streamlit/pages/1_triage_workbench.py`
- `drivers/ui/streamlit/widgets/bundle_viewer.py`
- `drivers/api/routes/triage.py`
- `app/interface_adapters/mappers/workbench_request_mapper.py`
- `app/interface_adapters/mappers/api_request_mapper.py`
- `app/interface_adapters/mappers/response_mapper.py`
- `app/interface_adapters/orchestrators/triage_graph_state.py`
- `app/interface_adapters/orchestrators/death_claim_triage_graph.py`
- `app/interface_adapters/orchestrators/death_claim_triage_orchestrator.py`

```python
# drivers/ui/streamlit/pages/1_triage_workbench.py
from app.interface_adapters.mappers.workbench_request_mapper import (
    WorkbenchRequestMapper,
)
from app.interface_adapters.presenters.triage_result_presenter import (
    TriageResultPresenter,
)


async def run_triage_workbench(selected_bundle, deps):
    request = WorkbenchRequestMapper().to_triage_request(selected_bundle)
    graph_state = TriageGraphState.from_request(request)
    result = await deps.death_claim_triage_graph.ainvoke(graph_state)
    return TriageResultPresenter().to_workbench_view(result)
```

```python
# app/interface_adapters/mappers/workbench_request_mapper.py
class WorkbenchRequestMapper:
    def to_triage_request(self, selected_bundle):
        return DeathClaimTriageRequest(
            bundle_id=selected_bundle.bundle_id,
            operator_id=selected_bundle.operator_id,
            source="triage_workbench",
        )
```

```python
# drivers/api/routes/triage.py
async def post_triage(request_body, deps):
    request = ApiRequestMapper().to_triage_request(request_body)
    graph_state = TriageGraphState.from_request(request)
    result = await deps.death_claim_triage_graph.ainvoke(graph_state)
    return ResponseMapper().to_api_response(result)
```

---

## Step 2: Normalize The Bundle And Assemble Context

### What happens

The workflow loads the intake bundle, normalizes the input artifacts, verifies policy context, and extracts the document facts needed for a grounded triage decision.

This is where the scenario’s narrower form of “RAG” appears: not an open-ended search experience, but grounded retrieval of policy/admin/document context relevant to the intake bundle.

### CA owner

- orchestrator
- use cases
- policy/document adapters

### Tree A files involved

- `app/interface_adapters/orchestrators/death_claim_triage_orchestrator.py`
- `app/use_cases/normalize_claim_bundle_uc.py`
- `app/use_cases/verify_policy_context_uc.py`
- `app/use_cases/extract_document_facts_uc.py`
- `app/adapters/policy_lookup/policy_lookup_adapter.py`
- `app/adapters/document_intake/document_intake_adapter.py`

```python
# app/interface_adapters/orchestrators/death_claim_triage_orchestrator.py
class DeathClaimTriageOrchestrator:
    async def handle(self, request):
        claim_bundle = self.normalize_claim_bundle_uc.execute(request.bundle_id)
        policy_context = self.verify_policy_context_uc.execute(claim_bundle)
        document_facts = self.extract_document_facts_uc.execute(claim_bundle)

        return await self._triage_bundle(
            claim_bundle=claim_bundle,
            policy_context=policy_context,
            document_facts=document_facts,
        )
```

```python
# app/use_cases/normalize_claim_bundle_uc.py
class NormalizeClaimBundleUC:
    def execute(self, bundle_id):
        raw_bundle = self.document_intake_adapter.load_bundle(bundle_id)
        return ClaimIntakeBundle.normalized_from(raw_bundle)
```

---

## Step 3: Tokenize PII Before External Model-Facing Analysis

### What happens

Before any external analysis step is invoked, claimant demographics and other raw PII are replaced with stable safe tokens. This preserves referential meaning for downstream artifact generation without allowing raw PII to cross the external model boundary.

### CA owner

- use cases
- safety adapters

### Tree A files involved

- `app/use_cases/tokenize_pii_for_model_uc.py`
- `app/use_cases/assemble_model_context_uc.py`
- `app/adapters/safety/pii_guardrail_adapter.py`
- `app/adapters/safety/token_mapper.py`

```python
# app/use_cases/tokenize_pii_for_model_uc.py
class TokenizePIIForModelUC:
    def execute(self, claim_bundle, policy_context, document_facts):
        safe_bundle = self.pii_guardrail_adapter.tokenize_claim_bundle(claim_bundle)
        safe_context = self.pii_guardrail_adapter.tokenize_context({
            "policy_context": policy_context,
            "document_facts": document_facts,
        })
        return safe_bundle, safe_context
```

### Why this matters here

This is not optional hardening. It is part of the scenario contract.

The exact tokenization implementation may vary later, but the architectural boundary is fixed:

- local extraction and tokenization before external analysis
- no raw claimant demographics or other raw PII sent externally

---

## Step 4: Assess Completeness And Ambiguity

### What happens

The system evaluates the normalized bundle and safe context to decide whether the case is:

- ready to proceed
- missing information
- ambiguous enough to require human review

### CA owner

- use cases
- orchestrator

### Tree A files involved

- `app/use_cases/assess_completeness_uc.py`
- `app/use_cases/detect_ambiguity_uc.py`

### Important note

The exact threshold that separates `missing information` from `ambiguous / HITL` is a **provisional assumption from [`deferred-hardening.md`](./deferred-hardening.md)**.

For this walkthrough, the assumption is:

- straightforward gaps become `request_more_information`
- conflicting or materially uncertain context becomes `escalate_to_human_review`

---

## Step 5: Assess Reviewability / Confidence Band

### What happens

The system converts the structured findings into a visible reviewability signal:

- `confidence_band`
- `reviewability_flags`
- `escalation_reasons`

The band is a summary. The reasons remain the primary gate.

### CA owner

- use cases
- safety/reviewability policy

### Tree A files involved

- `app/use_cases/assess_reviewability_uc.py`
- `app/use_cases/decide_triage_disposition_uc.py`
- `app/adapters/safety/reviewability_policy.py`

```python
# app/use_cases/assess_reviewability_uc.py
class AssessReviewabilityUC:
    def execute(self, completeness_assessment, ambiguity_assessment):
        return self.reviewability_policy.assess(
            completeness_assessment=completeness_assessment,
            ambiguity_assessment=ambiguity_assessment,
        )
```

```python
# app/use_cases/decide_triage_disposition_uc.py
class DecideTriageDispositionUC:
    def execute(self, completeness_assessment, ambiguity_assessment, reviewability):
        if reviewability.confidence_band == "Low":
            return TriageDisposition.escalate_to_human_review()

        if ambiguity_assessment.requires_human_review:
            return TriageDisposition.escalate_to_human_review()

        if completeness_assessment.is_missing_required_items:
            return TriageDisposition.request_more_information()

        return TriageDisposition.proceed()
```

### Important note

The exact reviewability rubric is a **provisional assumption from [`deferred-hardening.md`](./deferred-hardening.md)**.

For this walkthrough:

- `High` means ready to proceed
- `Medium` means bounded but still requires follow-up
- `Low` means escalate to human review

---

## Step 6: Generate The Correct Artifact Set

### What happens

Once the bounded disposition is chosen, the system generates the artifact set for that path.

### CA owner

- use cases
- model adapters
- safety adapters

### Tree A files involved

- `app/use_cases/generate_case_summary_uc.py`
- `app/use_cases/generate_requirements_checklist_uc.py`
- `app/use_cases/generate_follow_up_message_uc.py`
- `app/use_cases/generate_routing_decision_uc.py`
- `app/use_cases/create_hitl_review_task_uc.py`
- `app/adapters/model/prompts/`
- `app/adapters/safety/claimant_message_policy.py`
- `app/adapters/safety/no_adjudication_validator.py`

```python
# app/interface_adapters/orchestrators/death_claim_triage_orchestrator.py
async def _triage_bundle(self, claim_bundle, policy_context, document_facts):
    safe_bundle, safe_context = self.tokenize_pii_for_model_uc.execute(
        claim_bundle,
        policy_context,
        document_facts,
    )
    model_context = self.assemble_model_context_uc.execute(
        safe_bundle,
        safe_context,
    )
    completeness = self.assess_completeness_uc.execute(model_context)
    ambiguity = self.detect_ambiguity_uc.execute(model_context)
    reviewability = self.assess_reviewability_uc.execute(completeness, ambiguity)
    disposition = self.decide_triage_disposition_uc.execute(
        completeness,
        ambiguity,
        reviewability,
    )

    if disposition.name == "proceed":
        summary = self.generate_case_summary_uc.execute(model_context)
        decision = self.generate_routing_decision_uc.execute(
            model_context,
            disposition,
            reviewability,
        )
        return TriageResult.proceed(summary, decision, reviewability)

    if disposition.name == "request_more_information":
        checklist = self.generate_requirements_checklist_uc.execute(model_context)
        follow_up = self.generate_follow_up_message_uc.execute(model_context, checklist)
        return TriageResult.request_more_information(
            checklist,
            follow_up,
            reviewability,
        )

    review_task = self.create_hitl_review_task_uc.execute(
        model_context,
        ambiguity,
        reviewability,
    )
    return TriageResult.escalate_to_human_review(review_task, reviewability)
```

### Artifact-specific notes

#### `CASE_SUMMARY` + `ROUTING_DECISION`

These artifacts support the proceed path and explain why the bundle is ready for the next step.

`ROUTING_DECISION` should include:

- `confidence_band`
- bounded decision rationale

#### `REQUIREMENTS_CHECKLIST` + `FOLLOW_UP_MESSAGE`

These artifacts support the missing-information path.

The exact tone rubric for `FOLLOW_UP_MESSAGE` is a **provisional assumption from [`deferred-hardening.md`](./deferred-hardening.md)**. For now, the expectation is:

- empathetic
- operationally appropriate
- bounded to missing-information follow-up
- non-adjudicative

This path can still remain non-HITL with:

- `confidence_band = Medium`
- visible `reviewability_flags`

#### `HITL_REVIEW_TASK`

This artifact supports the ambiguous/HITL path and gives the reviewer a bounded rationale for why the case needs human attention.

It should include:

- `confidence_band = Low`
- explicit `escalation_reasons`

---

## Step 7: Validate, Present, And Hand Off

### What happens

Before the result is shown or queued, the generated artifacts are validated for policy and release suitability. Then they are presented in the workbench or routed to the review queue.

### CA owner

- validation use cases
- presenters
- review queue adapter

### Tree A files involved

- `app/use_cases/validate_follow_up_output_uc.py`
- `app/use_cases/validate_routing_rationale_uc.py`
- `app/interface_adapters/presenters/triage_result_presenter.py`
- `app/adapters/review_queue/review_queue_adapter.py`

```python
# app/use_cases/validate_follow_up_output_uc.py
class ValidateFollowUpOutputUC:
    def execute(self, follow_up_request):
        self.claimant_message_policy.assert_empathetic_and_operational(follow_up_request)
        self.no_adjudication_validator.assert_no_benefit_language(follow_up_request)
        return follow_up_request
```

```python
# app/interface_adapters/presenters/triage_result_presenter.py
class TriageResultPresenter:
    def to_workbench_view(self, triage_result):
        return {
            "disposition": triage_result.disposition,
            "confidence_band": triage_result.confidence_band,
            "reviewability_flags": triage_result.reviewability_flags,
            "escalation_reasons": triage_result.escalation_reasons,
            "case_summary": triage_result.case_summary,
            "requirements_checklist": triage_result.requirements_checklist,
            "follow_up_message": triage_result.follow_up_message,
            "routing_decision": triage_result.routing_decision,
            "hitl_review_task": triage_result.hitl_review_task,
        }
```

### Presenter responsibility

Presenters may:

- shape the output for the workbench
- remove internal-only details
- attach trace or review metadata

Presenters should not:

- decide whether the case is ambiguous
- decide whether the output is safe to release
- take over the no-adjudication or privacy boundary logic

---

## Traceable Path For Each Representative Case

### Case A: Complete Intake

1. `drivers/ui/streamlit/pages/1_triage_workbench.py`
2. `workbench_request_mapper.py`
3. `death_claim_triage_orchestrator.py`
4. `normalize_claim_bundle_uc.py`
5. `verify_policy_context_uc.py`
6. `tokenize_pii_for_model_uc.py`
7. `assess_completeness_uc.py`
8. `detect_ambiguity_uc.py`
9. `assess_reviewability_uc.py`
10. `generate_case_summary_uc.py`
11. `generate_routing_decision_uc.py`
12. `triage_result_presenter.py`

### Case B: Missing Information

1. `drivers/ui/streamlit/pages/1_triage_workbench.py`
2. `death_claim_triage_orchestrator.py`
3. `assess_completeness_uc.py`
4. `assess_reviewability_uc.py`
5. `decide_triage_disposition_uc.py`
6. `generate_requirements_checklist_uc.py`
7. `generate_follow_up_message_uc.py`
8. `validate_follow_up_output_uc.py`
9. `triage_result_presenter.py`

### Case C: Ambiguous / HITL

1. `drivers/ui/streamlit/pages/1_triage_workbench.py`
2. `death_claim_triage_orchestrator.py`
3. `detect_ambiguity_uc.py`
4. `assess_reviewability_uc.py`
5. `decide_triage_disposition_uc.py`
6. `create_hitl_review_task_uc.py`
7. `review_queue_adapter.py`
8. `review_queue_presenter.py`

---

## The Same Scenario Through Other Drivers

### Internal workbench UI

This is the primary demo surface in the current minimal steel thread:

- `drivers/ui/streamlit/pages/1_triage_workbench.py`

### API / internal service boundary

This is also in the current minimal steel thread and exposes the same workflow to internal services or automation:

- `drivers/api/routes/triage.py`
- `drivers/api/schemas/death_claim_request.py`
- `drivers/api/schemas/death_claim_response.py`

### Worker / background processing

This is a broader Tree A expansion path, not part of the current minimal steel thread. It can be added later for async review-queue and evaluation flows:

- `drivers/worker/tasks/process_triage_run.py`
- `drivers/worker/tasks/enqueue_review_task.py`
- `drivers/worker/tasks/run_eval_suite.py`

The business flow should remain the same across all of these surfaces when they exist.

---

## What This Example Makes Clear

In Tree A, the death-claim triage scenario fits if:

- the workshop spec stays the upstream contract
- PII tokenization is treated as a real boundary before external analysis
- completeness and ambiguity live in use cases and orchestrators
- reviewability is visible as a `confidence_band` plus explicit reasons
- claimant-facing follow-up remains bounded and non-adjudicative
- review-queue handoff remains explicit
- the unresolved details in [`deferred-hardening.md`](./deferred-hardening.md) are treated as intentional hardening work, not as if they were already settled

That is the core claim this downstream example is intended to test.
