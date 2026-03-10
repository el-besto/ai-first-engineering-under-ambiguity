# Death-Claim Workshop Spec

> **Purpose:** Capture the workshop-level, stakeholder-approved scenario contract before vertical-slice architecture, file placement, or framework-specific design.

---

**Status:** Active PoC planning artifact

This file is the **upstream PoC scenario contract** for the current death-claim planning work.

Use this document to:

- iterate on 1-3 realistic stakeholder scenarios
- keep those scenarios high-level enough for workshop discussion
- express the desired behavior as a compact executable-spec sketch with fakes
- avoid premature commitment to detailed Tree A file placement, LangGraph, DSPy, or framework-specific structure

Only after one scenario here is stable should it be translated into:

- a vertical slice
- a Tree A worked example
- a structural or code-placement walkthrough

---

## Source Grounding

This draft is grounded in:

1. [process-understanding.md](process-understanding.md)
2. [steel-thread.md](steel-thread.md)
3. [../pii-anonymization-w-dspy-hashing.md](../pii-anonymization-w-dspy-hashing.md)

This document is intentionally **higher-level** than:

- [`tree-a-code-map.md`](./tree-a-code-map.md)
- [`tree-a-worked-example.md`](./tree-a-worked-example.md)

Those are downstream design artifacts. This file comes first.

**Deferred hardening register:** [`deferred-hardening.md`](./deferred-hardening.md)

- Use the defer register to track known unknowns that are intentionally deferred while this scenario is translated downstream.

---

## How To Use This File

1. Start with one realistic scenario and one representative request bundle.
2. Keep the assertions stakeholder-readable.
3. Use fake collaborators only.
4. Capture non-negotiables and open questions explicitly.
5. Do not decide architecture here unless the workshop truly forces it.
6. When one scenario is stable enough, graduate it into a vertical-slice design artifact.

This file should not become:

- a file tree
- a graph design
- a DSPy implementation note
- a LangGraph node plan
- a detailed coding task list

---

## Canonical Workshop Scenario 01

### Death-Claim Intake + Next-Step Orchestration

#### Business context

Claims operations teams need a fast, clear way to triage new death-claim submissions, identify what is missing, and distinguish straightforward cases from those that require a human review checkpoint.

The goal is not to adjudicate a claim. The goal is to convert a raw intake bundle into a bounded next-step decision with useful operational artifacts.

#### Primary user

- `Claims operations specialist`

#### Other stakeholders

- `Claimant or beneficiary`
- `Downstream human reviewer / exception handler`
- `Governance / compliance`
- `Data science / evaluation`
- `Engineering / platform`
- supporting systems:
  - `Policy admin lookup`
  - `Document intake / storage`
  - `Review queue`

---

## Stakeholder Concerns And Non-Negotiables

### Claims operations specialist

- needs a clear completeness assessment, not just a generic summary
- needs an explicit next-step recommendation
- needs a concise rationale for proceed vs request-more-info vs escalate
- needs a visible reviewability signal, not just a hidden internal decision

### Claimant or beneficiary

- must receive follow-up requests in an empathetic, operationally appropriate tone
- should not be subjected to unnecessary repeated outreach when the missing items can be stated clearly the first time

### Governance / compliance

- the PoC must not adjudicate the claim or determine benefits
- human review boundaries must remain explicit
- raw demographics and other PII from the claim package must not be sent to external model calls
- model-facing text must be tokenized or pseudonymized before external analysis

### Data science / evaluation

- the system should produce outputs that can be reviewed for usefulness and consistency
- escalation behavior should be inspectable
- the distinction between complete, missing-information, and ambiguous cases should be testable
- reviewability reasons should be inspectable, not just summarized in a single opaque score

### Engineering / platform

- the scenario should be testable with fakes first
- the workflow should expose clear boundaries to policy lookup, document intake, and review-queue systems
- the workshop spec should not force implementation commitments prematurely

---

## Non-Negotiable Guardrails

- The PoC must not adjudicate claims.
- The PoC must not imply benefit determination or payout authority.
- Human review boundaries must stay explicit.
- Claimant-facing artifacts must use empathetic operational tone.
- Raw PII must not cross the external model boundary.
- PII handling should preserve referential meaning through stable safe tokens so the system can still produce useful artifacts.

### PII Rule In Workshop Terms

The workshop-level assertion is:

- given a claim package containing claimant demographics and other PII
- when the system prepares model-facing context
- then those values are replaced with stable safe tokens before external model analysis
- and the resulting artifacts can still be mapped back to the original records by a bounded secure process

Implementation reference, intentionally brief:

- local extraction and anonymization happen before external model analysis
- deterministic tokenization preserves referential meaning
- raw PII never crosses the external model boundary

---

## Representative Cases

### Case A: Complete Intake

**Artifacts**

- `CUSTOMER_REQUEST`
- `POLICY_SUMMARY`
- `CLAIM_INTAKE_FORM`

**Expected result**

- `CASE_SUMMARY`
- `ROUTING_DECISION` that is non-escalated
- `confidence_band = High`
- clear explanation of why the case is ready for the next step

### Case B: Missing Information

**Artifacts**

- `CUSTOMER_REQUEST`
- `POLICY_SUMMARY`
- `CLAIM_INTAKE_FORM`

**Expected result**

- `REQUIREMENTS_CHECKLIST`
- `FOLLOW_UP_MESSAGE`
- `confidence_band = Medium`
- `reviewability_flags` explaining why follow-up is still bounded and non-HITL
- explicit statement of what is missing and why it blocks progress

### Case C: Ambiguous / HITL

**Artifacts**

- `CUSTOMER_REQUEST`
- `POLICY_SUMMARY`
- `CLAIM_INTAKE_FORM`
- `DEATH_CERTIFICATE`
- `BENEFICIARY_RECORD`

**Expected result**

- `HITL_REVIEW_TASK`
- `confidence_band = Low`
- `escalation_reasons`
- escalation rationale
- any associated follow-up guidance needed by the reviewer

---

## Scenario Contract

### Given

- a claims operations specialist opens an internal workbench for a death-claim intake bundle
- the bundle may contain incomplete information, ambiguous beneficiary context, and PII
- the system can reference policy context and review-queue behavior through fake collaborators

### When

- the specialist asks the PoC to assess completeness and recommend the next operational step

### Then

- the system produces one bounded disposition:
  - proceed
  - request more information
  - escalate to human review
- the system generates the correct downstream artifact(s) for that disposition
- the system exposes a visible `confidence_band`
- the system exposes explicit `escalation_reasons` or `reviewability_flags`
- the rationale is understandable to operations and downstream reviewers
- claimant-facing follow-up language remains empathetic and bounded
- raw PII does not cross the external model boundary
- the PoC does not cross into adjudication or benefits determination

---

## Compact Pytest-Style Workshop Sketch

This is intentionally **not** a final architecture sketch. It is a workshop-readable executable-spec shape.

```python
@pytest.mark.feature("death_claim_intake_triage")
class TestDeathClaimIntakeWorkshopSpec:
    """
    Workshop contract for death-claim intake + next-step orchestration.

    This test is meant to be discussed with stakeholders before committing
    to a vertical slice or framework-specific architecture.
    """

    async def test_triage_representative_claim_cases(
        self,
        triage_workflow,
        fake_policy_lookup,
        fake_document_store,
        fake_review_queue,
        fake_pii_guardrail,
        fake_evaluation_recorder,
    ):
        # Case A: complete intake
        complete_case = ClaimIntakeBundle.fake_complete()
        complete_result = await triage_workflow.assess(complete_case)

        assert complete_result.disposition == "proceed"
        assert complete_result.confidence_band == "High"
        assert complete_result.case_summary
        assert complete_result.routing_decision
        assert not complete_result.escalation_reasons
        assert not complete_result.hitl_review_task

        # Case B: missing information
        missing_info_case = ClaimIntakeBundle.fake_missing_information()
        missing_result = await triage_workflow.assess(missing_info_case)

        assert missing_result.disposition == "request_more_information"
        assert missing_result.confidence_band == "Medium"
        assert missing_result.requirements_checklist
        assert missing_result.follow_up_message
        assert missing_result.reviewability_flags
        assert missing_result.escalation_reasons == []
        assert "empathetic" in missing_result.follow_up_message_quality_markers

        # Case C: ambiguous / HITL
        ambiguous_case = ClaimIntakeBundle.fake_ambiguous()
        ambiguous_result = await triage_workflow.assess(ambiguous_case)

        assert ambiguous_result.disposition == "escalate_to_human_review"
        assert ambiguous_result.confidence_band == "Low"
        assert ambiguous_result.hitl_review_task
        assert ambiguous_result.escalation_reasons
        assert ambiguous_result.escalation_rationale

        # Governance / compliance assertion
        assert fake_pii_guardrail.external_model_input_contains_no_raw_pii()
        assert fake_pii_guardrail.used_stable_safe_tokens()

        # Scope boundary assertion
        assert "adjudication" not in complete_result.routing_decision.lower()
        assert "benefit determination" not in ambiguous_result.escalation_rationale.lower()

        # Evaluation / observability assertion
        assert fake_evaluation_recorder.recorded_case("complete")
        assert fake_evaluation_recorder.recorded_case("missing_information")
        assert fake_evaluation_recorder.recorded_case("ambiguous")
```

### What the sketch is trying to prove

- one workflow can distinguish the three representative cases
- the outputs are operationally useful, not generic
- privacy and HITL boundaries are visible to stakeholders
- reviewability is visible as a band plus explicit reasons
- the workshop can iterate on behavior before implementation details are locked

### What the sketch is explicitly not deciding

- whether the workflow is implemented with LangGraph
- whether DSPy is used in any internal guardrail or extraction step
- where the files live in the local Tree A steel thread
- whether the final delivery surface is Streamlit, Reflex, FastAPI, or a combination

---

## Open Questions For The Next Workshop Loop

The highest-priority intentional deferments are tracked in [`deferred-hardening.md`](./deferred-hardening.md).

- What exact fields count as prohibited raw PII for external model-facing context in this scenario?
- What exact conditions separate `missing information` from `ambiguous / HITL`?
- What tone markers must be visible in a claimant-facing follow-up draft?
- What minimum explanation is required in a routing or escalation rationale?
- What reviewable metrics would data science or governance want to see in the demo?
- What exact reviewability rubric should produce `High / Medium / Low` confidence bands?

These should be refined in the workshop before the scenario is translated into local implementation-planning artifacts.

---

## Graduation Criteria

This scenario is ready to drive a vertical slice when:

1. stakeholders agree the three representative cases are the right minimum set
2. the disposition rules are clear enough that workshop participants can tell when the system is wrong
3. the artifact outputs are specific enough to review in a demo
4. the PII boundary is explicit enough to test
5. the scope boundary against adjudication is explicit enough to test

Once those are true, this scenario can graduate into:

- a Tree A worked example
- a vertical-slice code map
- finer-grained acceptance and integration test design

---

## Downstream Handoff

When this scenario is mature enough, the next design step is **not** to add more workshop detail here.

The next step is to translate the scenario into downstream artifacts such as:

- [`steel-thread.md`](./steel-thread.md)
- [`tree-a-code-map.md`](./tree-a-code-map.md)
- [`tree-a-worked-example.md`](./tree-a-worked-example.md)

That is where file placement, vertical slices, and implementation tradeoffs should be made visible, while respecting the intentional deferments tracked in [`deferred-hardening.md`](./deferred-hardening.md).
