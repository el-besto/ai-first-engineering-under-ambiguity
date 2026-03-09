# Insurance Process Candidates

## Purpose

This document catalogs candidate insurance workflows for PoC selection. It is intended to support a narrow, defensible choice for the Bestow AI take-home by comparing options across product relevance, AI fit, implementation simplicity, demo strength, and artifact burden.

## Evaluation Criteria

- Bestow relevance
- Life-insurance specificity
- Agentic AI leverage
- Prototype simplicity
- Fixture burden
- Simple-case automation viability
- Escalated-case HITL viability
- 5-minute demo strength
- Compliance / decision-risk profile

## Common Artifact Inventory

This inventory defines reusable artifact types that may appear as inputs, intermediates, or outputs across candidate processes. The goal is to estimate fixture burden early and avoid repeating the same document descriptions under every process.

| Artifact ID             | Artifact name                  | Type                       | Typical source                  | Fake complexity | Notes                                              |
|-------------------------|--------------------------------|----------------------------|---------------------------------|-----------------|----------------------------------------------------|
| CUSTOMER_REQUEST        | Customer or claimant request   | structured record          | portal submission / call center | Low             | Basic intent and identifying details               |
| POLICY_SUMMARY          | Policy snapshot                | structured record          | policy admin system             | Low             | Policy number, status, insured, and basic coverage |
| CLAIM_INTAKE_FORM       | Claim intake form              | document / structured form | claimant or support rep         | Low             | Can be modeled as JSON or a simple form            |
| DEATH_CERTIFICATE       | Death certificate              | document                   | claimant upload                 | Medium          | Can be synthetic and simplified                    |
| BENEFICIARY_RECORD      | Beneficiary record             | structured record          | policy admin system             | Low             | Used for validation and follow-up context          |
| APPLICATION_SUMMARY     | Insurance application snapshot | structured record          | application system              | Low             | Useful for underwriting and issue workflows        |
| UNDERWRITING_CASE_NOTES | Underwriting notes             | document / note set        | underwriting workbench          | Medium          | Good candidate for summarization                   |
| MEDICAL_EVIDENCE        | APS / medical evidence         | document                   | external evidence source        | High            | High burden; avoid unless process needs it         |
| SERVICE_REQUEST_FORM    | Policy service request         | structured form            | portal / service rep            | Low             | Good for servicing workflows                       |
| REQUIREMENTS_CHECKLIST  | Missing-info checklist         | generated artifact         | system-generated                | Low             | Common intermediate artifact                       |
| CASE_SUMMARY            | Case summary                   | generated artifact         | AI-generated                    | Low             | Common intermediate artifact                       |
| ROUTING_DECISION        | Routing / disposition record   | generated artifact         | AI + rules                      | Low             | Straight-through vs HITL                           |
| FOLLOW_UP_MESSAGE       | Draft communication            | generated artifact         | AI-generated                    | Low             | Email, portal, or task note                        |
| HITL_REVIEW_TASK        | Human review task              | task / work item           | system-generated                | Low             | Escalation artifact                                |

## Candidate Summary Table

| Process                                                    | Primary user                       | Life-insurance specificity | Agentic AI fit | Prototype complexity | Fixture burden | Simple-case automation | HITL escalation fit | Demo strength | Bestow relevance | Recommendation rank |
|------------------------------------------------------------|------------------------------------|----------------------------|----------------|----------------------|----------------|------------------------|---------------------|---------------|------------------|---------------------|
| Death claim intake + next-step orchestration               | Claims ops / claimant support      | High                       | High           | Medium               | Medium         | Strong                 | Strong              | High          | High             | 1                   |
| Underwriting case triage / underwriter copilot             | Underwriter                        | High                       | High           | Medium               | Medium         | Moderate               | Strong              | High          | High             | 2                   |
| Policy servicing request intake and routing                | Service ops / policyholder support | Medium                     | High           | Low                  | Low            | Strong                 | Strong              | High          | High             | 3                   |
| Application completion / abandoned application rescue      | Applicant growth / service ops     | Medium                     | High           | Low                  | Low            | Strong                 | Moderate            | High          | High             | 4                   |
| Claim requirements tracking / beneficiary follow-up        | Claims ops                         | High                       | High           | Medium               | Medium         | Moderate               | Strong              | Medium        | Medium           | 5                   |
| Beneficiary change request review                          | Service ops                        | High                       | Medium         | Medium               | Medium         | Moderate               | Strong              | Medium        | Medium           | 6                   |
| Post-issue audit assistant                                 | Underwriting audit / risk ops      | High                       | High           | Medium               | Medium         | Moderate               | Strong              | Medium        | High             | 7                   |
| Medical record / APS summarization                         | Underwriter                        | High                       | High           | High                 | High           | Weak                   | Strong              | Medium        | High             | 8                   |
| Policy issue / bind exception resolver                     | New business ops                   | Medium                     | Medium         | Medium               | Medium         | Moderate               | Moderate            | Medium        | Medium           | 9                   |
| Billing / payment exception and lapse-prevention assistant | Billing / service ops              | Low                        | Medium         | Low                  | Low            | Strong                 | Moderate            | Medium        | Medium           | 10                  |

## Candidate 1: Death claim intake + next-step orchestration

### Summary

- One-line description: Guide a beneficiary or internal operator through initial death-claim intake, validate completeness, and generate the next operational steps.
- Primary user: Claims operations specialist or claimant support representative
- Trigger event: A death claim is initiated by a beneficiary, family member, or support team
- Core output: Structured intake record, missing-item checklist, and routed follow-up tasks

### Why It Matters

- Current pain point: Claim initiation is often confusing, document-heavy, and emotionally difficult, which increases incomplete submissions and manual follow-up.
- Why AI/agentic helps: AI can guide intake, summarize what was provided, identify gaps, and coordinate the next actions without making the claim decision itself.

### Lean Evaluation

- Life-insurance specificity: High
- Bestow relevance: High
- Prototype complexity: Medium
- Fixture burden: Medium
- Simple-case automation viability: Strong
- Escalated-case HITL viability: Strong
- Demo strength: High
- Compliance / operational risk: Medium

### Agentic Opportunity

- Extraction, summarization, classification, next-step orchestration, communication drafting
- Human-in-loop checkpoint: Claims specialist reviews completeness assessment and any claimant-facing communication before downstream action

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`
- Notes: Enough to validate a basic claim submission and propose a straight-through next step

**Escalated / HITL case**

- Artifact IDs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`, `DEATH_CERTIFICATE`, `BENEFICIARY_RECORD`
- Notes: Add missing details, record mismatches, or beneficiary ambiguity to trigger human review

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `REQUIREMENTS_CHECKLIST`, `ROUTING_DECISION`, `FOLLOW_UP_MESSAGE`, `HITL_REVIEW_TASK`
- Notes: The system should explain completeness, missing items, and whether the case can proceed automatically or needs review

#### Expected Outputs

- Artifact IDs: `ROUTING_DECISION`, `REQUIREMENTS_CHECKLIST`, `FOLLOW_UP_MESSAGE`
- Notes: The visible end state is an intake disposition plus next-step communication

### Notes

- Systems touched: Claim intake forms, document storage, task queue, policy lookup
- Key downside or watchout: Must be framed as intake/orchestration support, not adjudication or benefits determination

## Candidate 2: Underwriting case triage / underwriter copilot

### Summary

- One-line description: Summarize underwriting evidence, identify missing information, and recommend the next review step for an underwriter.
- Primary user: Underwriter
- Trigger event: A new or in-progress underwriting case requires review
- Core output: Case summary, missing evidence list, and recommended next action

### Why It Matters

- Current pain point: Underwriting work is fragmented across forms, evidence, third-party data, and notes, causing slow manual review.
- Why AI/agentic helps: AI can consolidate case context, flag gaps, and reduce time spent assembling the review picture.

### Lean Evaluation

- Life-insurance specificity: High
- Bestow relevance: High
- Prototype complexity: Medium
- Fixture burden: Medium
- Simple-case automation viability: Moderate
- Escalated-case HITL viability: Strong
- Demo strength: High
- Compliance / operational risk: High

### Agentic Opportunity

- Summarization, extraction, classification, next-best-action recommendation
- Human-in-loop checkpoint: Underwriter confirms all recommendations and retains decision authority

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `APPLICATION_SUMMARY`, `UNDERWRITING_CASE_NOTES`
- Notes: A thin slice can work with a compact application snapshot and a short note bundle

**Escalated / HITL case**

- Artifact IDs: `APPLICATION_SUMMARY`, `UNDERWRITING_CASE_NOTES`, `MEDICAL_EVIDENCE`
- Notes: Richer evidence or inconsistent information should trigger underwriter review

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `REQUIREMENTS_CHECKLIST`, `ROUTING_DECISION`, `HITL_REVIEW_TASK`
- Notes: The AI should summarize the case, highlight gaps, and recommend the next review path

#### Expected Outputs

- Artifact IDs: `CASE_SUMMARY`, `ROUTING_DECISION`, `REQUIREMENTS_CHECKLIST`
- Notes: The visible output is a concise underwriter-facing triage packet

### Notes

- Systems touched: Application record, underwriting evidence, third-party data sources, work queue
- Key downside or watchout: Needs careful framing to avoid appearing like automated risk selection

## Candidate 3: Policy servicing request intake and routing

### Summary

- One-line description: Accept a policy servicing request, classify it, gather required context, and route it to self-service, straight-through processing, or operations review.
- Primary user: Service operations specialist or digital servicing support
- Trigger event: A policyholder submits a service request
- Core output: Classified request, collected context, and routing decision

### Why It Matters

- Current pain point: Servicing requests are varied, repetitive, and often arrive incomplete, creating unnecessary manual back-and-forth.
- Why AI/agentic helps: AI can interpret intent, ask for missing details, and direct the work into the right handling path.

### Lean Evaluation

- Life-insurance specificity: Medium
- Bestow relevance: High
- Prototype complexity: Low
- Fixture burden: Low
- Simple-case automation viability: Strong
- Escalated-case HITL viability: Strong
- Demo strength: High
- Compliance / operational risk: Medium

### Agentic Opportunity

- Classification, extraction, guided intake, orchestration, drafting
- Human-in-loop checkpoint: Operations review for exceptions, policy changes, or non-standard requests

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `SERVICE_REQUEST_FORM`
- Notes: This is one of the lightest-weight input sets and easiest to fake cleanly

**Escalated / HITL case**

- Artifact IDs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `SERVICE_REQUEST_FORM`
- Notes: Ambiguity, conflicting fields, or out-of-policy requests can trigger HITL without adding many new artifacts

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `ROUTING_DECISION`, `FOLLOW_UP_MESSAGE`, `HITL_REVIEW_TASK`
- Notes: This process naturally produces classification, routing, and exception handling artifacts

#### Expected Outputs

- Artifact IDs: `ROUTING_DECISION`, `FOLLOW_UP_MESSAGE`
- Notes: The end state is a clear servicing path and any required follow-up communication

### Notes

- Systems touched: Customer portal, policy administration system, service queue, knowledge base
- Key downside or watchout: Can feel generic unless anchored to life-specific request types

## Candidate 4: Application completion / abandoned application rescue

### Summary

- One-line description: Re-engage incomplete applicants, explain blockers, and guide them to the next required step.
- Primary user: Applicant growth or service operations team
- Trigger event: An application is started but not completed
- Core output: Applicant-specific recovery plan and guided next-step workflow

### Why It Matters

- Current pain point: Abandoned applications reduce conversion and require manual follow-up to recover.
- Why AI/agentic helps: AI can explain what is missing, answer context-sensitive questions, and coordinate follow-up messaging.

### Lean Evaluation

- Life-insurance specificity: Medium
- Bestow relevance: High
- Prototype complexity: Low
- Fixture burden: Low
- Simple-case automation viability: Strong
- Escalated-case HITL viability: Moderate
- Demo strength: High
- Compliance / operational risk: Low

### Agentic Opportunity

- Classification, FAQ response, drafting, orchestration
- Human-in-loop checkpoint: Growth or service team reviews non-standard or sensitive recovery workflows

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `APPLICATION_SUMMARY`, `CUSTOMER_REQUEST`
- Notes: A minimal stalled application snapshot is enough to drive a guided recovery flow

**Escalated / HITL case**

- Artifact IDs: `APPLICATION_SUMMARY`, `CUSTOMER_REQUEST`, `HITL_REVIEW_TASK`
- Notes: Escalation is more likely to come from exception flags than from additional document burden

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `ROUTING_DECISION`, `FOLLOW_UP_MESSAGE`
- Notes: The workflow centers on identifying the blocker and generating the right next-step messaging

#### Expected Outputs

- Artifact IDs: `FOLLOW_UP_MESSAGE`, `ROUTING_DECISION`
- Notes: The visible result is a recovery recommendation and applicant-facing next step

### Notes

- Systems touched: Application flow, CRM, messaging, customer portal
- Key downside or watchout: Slightly weaker operations depth than claims or underwriting

## Candidate 5: Claim requirements tracking / beneficiary follow-up

### Summary

- One-line description: Track claim requirements after intake, identify missing items, and manage beneficiary follow-up.
- Primary user: Claims operations specialist
- Trigger event: A claim has been opened but is not yet fully documented
- Core output: Requirements status, follow-up plan, and beneficiary-facing summaries

### Why It Matters

- Current pain point: Claims often stall because missing requirements are not obvious or consistently communicated.
- Why AI/agentic helps: AI can monitor requirement state, summarize the outstanding work, and draft targeted follow-ups.

### Lean Evaluation

- Life-insurance specificity: High
- Bestow relevance: Medium
- Prototype complexity: Medium
- Fixture burden: Medium
- Simple-case automation viability: Moderate
- Escalated-case HITL viability: Strong
- Demo strength: Medium
- Compliance / operational risk: Medium

### Agentic Opportunity

- Summarization, checklist generation, drafting, task orchestration
- Human-in-loop checkpoint: Claims team approves outbound communication and exception handling

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `CLAIM_INTAKE_FORM`, `POLICY_SUMMARY`, `BENEFICIARY_RECORD`
- Notes: A partially documented claim can still produce a useful requirements tracker

**Escalated / HITL case**

- Artifact IDs: `CLAIM_INTAKE_FORM`, `POLICY_SUMMARY`, `BENEFICIARY_RECORD`, `DEATH_CERTIFICATE`
- Notes: Additional evidence gaps or mismatches create a stronger review path

#### Expected Intermediate Artifacts

- Artifact IDs: `REQUIREMENTS_CHECKLIST`, `CASE_SUMMARY`, `FOLLOW_UP_MESSAGE`, `HITL_REVIEW_TASK`
- Notes: This workflow is fundamentally about managing unresolved requirements

#### Expected Outputs

- Artifact IDs: `REQUIREMENTS_CHECKLIST`, `FOLLOW_UP_MESSAGE`
- Notes: The end state is a clear list of missing items and the next beneficiary communication

### Notes

- Systems touched: Claim record, document repository, communication tools, work queue
- Key downside or watchout: Slightly less intuitive than initial intake as a first demo

## Candidate 6: Beneficiary change request review

### Summary

- One-line description: Review beneficiary change requests for completeness and route straightforward updates versus exceptions.
- Primary user: Policy service operations specialist
- Trigger event: A beneficiary change request is submitted
- Core output: Completeness summary, exception flags, and servicing recommendation

### Why It Matters

- Current pain point: Change requests are operationally repetitive but sensitive, and errors lead to delays or rework.
- Why AI/agentic helps: AI can interpret forms, surface missing or conflicting fields, and standardize handling.

### Lean Evaluation

- Life-insurance specificity: High
- Bestow relevance: Medium
- Prototype complexity: Medium
- Fixture burden: Medium
- Simple-case automation viability: Moderate
- Escalated-case HITL viability: Strong
- Demo strength: Medium
- Compliance / operational risk: High

### Agentic Opportunity

- Extraction, classification, summarization, routing
- Human-in-loop checkpoint: Service operations specialist validates any change before the system of record is updated

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `POLICY_SUMMARY`, `SERVICE_REQUEST_FORM`, `BENEFICIARY_RECORD`
- Notes: A basic change request can be reviewed with a small, tractable set of inputs

**Escalated / HITL case**

- Artifact IDs: `POLICY_SUMMARY`, `SERVICE_REQUEST_FORM`, `BENEFICIARY_RECORD`, `HITL_REVIEW_TASK`
- Notes: Exceptions typically stem from conflicting details, missing confirmation, or policy constraints

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `ROUTING_DECISION`, `REQUIREMENTS_CHECKLIST`, `HITL_REVIEW_TASK`
- Notes: The AI can summarize completeness and signal whether review is needed

#### Expected Outputs

- Artifact IDs: `ROUTING_DECISION`, `REQUIREMENTS_CHECKLIST`
- Notes: The visible result is a review outcome plus any missing information checklist

### Notes

- Systems touched: Customer portal, document intake, policy administration system
- Key downside or watchout: Sensitive enough that you need to keep business rules intentionally light

## Candidate 7: Post-issue audit assistant

### Summary

- One-line description: Support post-issue audits by retrieving case evidence, summarizing discrepancies, and preparing review packets.
- Primary user: Underwriting audit or risk operations specialist
- Trigger event: A policy enters post-issue review
- Core output: Audit summary, evidence map, and exception flags

### Why It Matters

- Current pain point: Post-issue review is document-heavy and time-consuming.
- Why AI/agentic helps: AI can assemble a coherent audit narrative and flag where reviewers should focus.

### Lean Evaluation

- Life-insurance specificity: High
- Bestow relevance: High
- Prototype complexity: Medium
- Fixture burden: Medium
- Simple-case automation viability: Moderate
- Escalated-case HITL viability: Strong
- Demo strength: Medium
- Compliance / operational risk: Medium

### Agentic Opportunity

- Retrieval, summarization, discrepancy detection, drafting
- Human-in-loop checkpoint: Auditor or underwriter reviews all flags and findings before action

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `APPLICATION_SUMMARY`, `UNDERWRITING_CASE_NOTES`, `POLICY_SUMMARY`
- Notes: A lightweight audit packet can be synthesized with application and policy snapshots

**Escalated / HITL case**

- Artifact IDs: `APPLICATION_SUMMARY`, `UNDERWRITING_CASE_NOTES`, `POLICY_SUMMARY`, `MEDICAL_EVIDENCE`
- Notes: Additional evidence or discrepancies increase realism but also fixture cost

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `REQUIREMENTS_CHECKLIST`, `HITL_REVIEW_TASK`
- Notes: The AI should surface discrepancies and produce a focused review packet

#### Expected Outputs

- Artifact IDs: `CASE_SUMMARY`, `HITL_REVIEW_TASK`
- Notes: The end state is an auditor-facing review summary and flagged task

### Notes

- Systems touched: Policy file, application record, evidence sources, audit queue
- Key downside or watchout: Bestow already publicly references AI in this area, so the idea may feel less differentiated

## Candidate 8: Medical record / APS summarization

### Summary

- One-line description: Summarize attending physician statements or medical records into underwriter-friendly highlights.
- Primary user: Underwriter
- Trigger event: Medical evidence is received for a case
- Core output: Timeline, condition summary, and flagged risk factors

### Why It Matters

- Current pain point: Medical evidence is dense, unstructured, and slow to review.
- Why AI/agentic helps: AI can compress long documents into actionable summaries and highlight important data for review.

### Lean Evaluation

- Life-insurance specificity: High
- Bestow relevance: High
- Prototype complexity: High
- Fixture burden: High
- Simple-case automation viability: Weak
- Escalated-case HITL viability: Strong
- Demo strength: Medium
- Compliance / operational risk: High

### Agentic Opportunity

- Extraction, summarization, highlighting, evidence mapping
- Human-in-loop checkpoint: Underwriter validates all summaries before they influence a case outcome

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `APPLICATION_SUMMARY`, `MEDICAL_EVIDENCE`
- Notes: Even the simple case requires richer source material than most other candidates

**Escalated / HITL case**

- Artifact IDs: `APPLICATION_SUMMARY`, `MEDICAL_EVIDENCE`, `UNDERWRITING_CASE_NOTES`
- Notes: Complex evidence interpretation almost always pushes this toward a HITL-heavy experience

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `REQUIREMENTS_CHECKLIST`, `HITL_REVIEW_TASK`
- Notes: The key artifact is a reliable evidence summary with flagged follow-up needs

#### Expected Outputs

- Artifact IDs: `CASE_SUMMARY`, `HITL_REVIEW_TASK`
- Notes: The visible output is an underwriter-facing evidence summary and escalation path

### Notes

- Systems touched: Medical evidence repository, underwriting workbench
- Key downside or watchout: Requires more realistic source material and careful handling of clinical nuance

## Candidate 9: Policy issue / bind exception resolver

### Summary

- One-line description: Identify blockers to policy issue or bind, gather missing items, and route exceptions for operational resolution.
- Primary user: New business operations specialist
- Trigger event: A policy is ready to issue but an exception blocks completion
- Core output: Exception summary, required actions, and routing plan

### Why It Matters

- Current pain point: Issue and bind workflows can stall on missing signatures, payment issues, or unresolved validations.
- Why AI/agentic helps: AI can normalize exception handling and coordinate operational next steps.

### Lean Evaluation

- Life-insurance specificity: Medium
- Bestow relevance: Medium
- Prototype complexity: Medium
- Fixture burden: Medium
- Simple-case automation viability: Moderate
- Escalated-case HITL viability: Moderate
- Demo strength: Medium
- Compliance / operational risk: Medium

### Agentic Opportunity

- Classification, summarization, drafting, orchestration
- Human-in-loop checkpoint: New business operations confirms any resolution path before policy issuance

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `APPLICATION_SUMMARY`, `POLICY_SUMMARY`, `CUSTOMER_REQUEST`
- Notes: A small set of issue-state records is enough to show exception resolution logic

**Escalated / HITL case**

- Artifact IDs: `APPLICATION_SUMMARY`, `POLICY_SUMMARY`, `CUSTOMER_REQUEST`, `HITL_REVIEW_TASK`
- Notes: Most escalations are driven by exception severity rather than heavy document burden

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `REQUIREMENTS_CHECKLIST`, `ROUTING_DECISION`, `FOLLOW_UP_MESSAGE`
- Notes: The AI can standardize the exception story and required next actions

#### Expected Outputs

- Artifact IDs: `ROUTING_DECISION`, `FOLLOW_UP_MESSAGE`, `REQUIREMENTS_CHECKLIST`
- Notes: The visible result is a clear issue-resolution path and any required outreach

### Notes

- Systems touched: Application record, payment systems, e-signature, policy administration
- Key downside or watchout: Harder to make immediately legible to a broad audience than claims or servicing

## Candidate 10: Billing / payment exception and lapse-prevention assistant

### Summary

- One-line description: Detect payment issues, explain the problem, and coordinate policyholder outreach or internal action to reduce lapse risk.
- Primary user: Billing or service operations specialist
- Trigger event: A payment failure, billing exception, or lapse-risk signal occurs
- Core output: Exception summary, recommended next action, and drafted outreach

### Why It Matters

- Current pain point: Billing issues are repetitive, time-sensitive, and often handled manually.
- Why AI/agentic helps: AI can standardize exception handling and reduce the time to customer communication.

### Lean Evaluation

- Life-insurance specificity: Low
- Bestow relevance: Medium
- Prototype complexity: Low
- Fixture burden: Low
- Simple-case automation viability: Strong
- Escalated-case HITL viability: Moderate
- Demo strength: Medium
- Compliance / operational risk: Medium

### Agentic Opportunity

- Classification, drafting, orchestration, summarization
- Human-in-loop checkpoint: Service or billing specialist reviews outreach for edge cases

### Artifact Footprint

#### Expected Inputs

**Simple case**

- Artifact IDs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`
- Notes: The simplest candidate to fake from a data burden perspective

**Escalated / HITL case**

- Artifact IDs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `HITL_REVIEW_TASK`
- Notes: Escalation can come from repeated failures, policy status complexity, or unsupported remediation paths

#### Expected Intermediate Artifacts

- Artifact IDs: `CASE_SUMMARY`, `ROUTING_DECISION`, `FOLLOW_UP_MESSAGE`
- Notes: The system mostly needs to classify the issue and prepare the right communication

#### Expected Outputs

- Artifact IDs: `FOLLOW_UP_MESSAGE`, `ROUTING_DECISION`
- Notes: The visible result is a lapse-prevention recommendation and drafted outreach

### Notes

- Systems touched: Billing system, CRM, policy administration, communication tools
- Key downside or watchout: Least differentiated as a life-insurance-specific workflow

## Artifact Burden Observations

- The lightest fixture burden candidates are policy servicing intake, application rescue, and billing exception handling because they rely mostly on structured records and generated artifacts rather than uploaded evidence.
- The heaviest synthetic evidence burden sits with medical record summarization and, to a lesser extent, underwriting triage or post-issue audit when richer evidence is introduced.
- The strongest candidates for a “simple automated case + escalated HITL case” demo are death claim intake, policy servicing intake, and underwriting triage because they support a clear shift from straightforward routing to human review without requiring a broad workflow engine.
- Underwriting triage remains technically strong, but it now carries higher novelty risk because the underwriting-workbench category already has familiar public demos.

## Shortlist

- Death claim intake + next-step orchestration
- Underwriting case triage / underwriter copilot
- Policy servicing request intake and routing

## Recommendation Snapshot

The strongest candidates at this stage are death claim intake, underwriting case triage, and policy servicing intake. Death claim intake has the clearest life-insurance identity and a strong agentic workflow shape while still supporting a plausible simple case and escalated case. Underwriting case triage remains strong technically, but it now has higher novelty risk because of the existing underwriting-workbench demo category, and its artifact burden rises quickly once medical evidence is introduced. Policy servicing intake is still the easiest to prototype and demo cleanly, with the lightest fixture burden of the top three.
