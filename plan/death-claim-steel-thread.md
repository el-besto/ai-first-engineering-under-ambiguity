# Death Claim Steel Thread

## Selected Direction

- Process: Death claim intake + next-step orchestration
- Scope: Intake + completeness triage
- Primary user: Claims operations specialist
- Secondary stakeholders: Claimant or beneficiary, downstream human reviewer
- Interaction model: Internal workbench with generated external follow-up outputs

## Problem Statement

Claims operations teams need a fast, clear way to triage new death-claim submissions, identify what is missing, and distinguish straightforward cases from those that require a human review checkpoint. The improvement opportunity is to reduce manual back-and-forth while making the triage rationale and next steps explicit.

## Success Criteria

- The prototype routes three representative claim cases into distinct dispositions
- The system produces a useful completeness assessment rather than a generic summary
- The missing-information case produces a clear checklist and claimant or beneficiary follow-up draft
- The ambiguous case produces a HITL review task with an understandable rationale
- The UI makes the case-state differences obvious in under 5 minutes of demo time
- The system does not imply autonomous claim adjudication or benefits determination

## Representative Cases

### Case A: Complete intake

- Artifacts: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`
- Expected result: Case summary and straightforward routing decision

### Case B: Missing information

- Artifacts: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`
- Expected result: Missing-items checklist and claimant or beneficiary follow-up draft

### Case C: Ambiguous / HITL

- Artifacts: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`, `DEATH_CERTIFICATE`, `BENEFICIARY_RECORD`
- Expected result: HITL review task, rationale, and any associated follow-up guidance

## Acceptance Criteria

- Given a complete intake bundle, when the graph processes the case, then it produces a summary and non-escalated routing decision
- Given an incomplete intake bundle, when the graph processes the case, then it identifies missing items and drafts a follow-up message
- Given an ambiguous intake bundle, when the graph processes the case, then it creates a HITL review task and explains why escalation is required

## Architecture Outline

### Streamlit surface

- Single internal workbench page
- Three tabs, one per representative case
- Panels for intake summary, completeness assessment, generated artifacts, and disposition

### LangGraph flow

1. Load and normalize the case bundle
2. Summarize claim context
3. Assess completeness and ambiguity
4. Route to one of:
   - proceed
   - request more information
   - escalate to human review
5. Generate downstream artifacts for the selected route

### Output artifacts

- `CASE_SUMMARY`
- `REQUIREMENTS_CHECKLIST`
- `ROUTING_DECISION`
- `FOLLOW_UP_MESSAGE`
- `HITL_REVIEW_TASK`

## Demo Rationale

This direction keeps the PoC differentiated from underwriting-workbench demos while still showing strong agentic orchestration, explicit human-in-the-loop boundaries, and a life-insurance-specific workflow with meaningful stakeholder interplay.
