# Synthetic Data Plan

## Purpose

This document identifies open-source synthetic-data sources for the PoC artifact inventory in [docs/references/insurance-processes.md](../docs/references/insurance-processes.md). The goal is to assemble believable demo fixtures for a narrow insurance workflow, not to build a production-grade data generation pipeline.

## Current Workflow Focus

- Selected workflow: Death claim intake + next-step orchestration
- Selected scope: Intake + completeness triage
- Workflow context: [death-claim-process-understanding.md](death-claim-process-understanding.md)
- Primary artifacts for the initial steel thread: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`
- Escalation artifacts for the ambiguous case: `DEATH_CERTIFICATE`, `BENEFICIARY_RECORD`
- Working strategy: use open synthetic insurance datasets for the structured intake artifacts, then hand-author a very small set of believable beneficiary and death-certificate fixtures for the HITL path

## Initial Fixture Bundle

### Case A: Complete intake

- Inputs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`
- Expected outcome: completeness assessment plus a straightforward routing decision

### Case B: Missing information

- Inputs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`
- Expected outcome: missing-items checklist plus claimant or beneficiary follow-up draft

### Case C: Ambiguous / HITL case

- Inputs: `CUSTOMER_REQUEST`, `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`, `DEATH_CERTIFICATE`, `BENEFICIARY_RECORD`
- Expected outcome: HITL review task with rationale, plus any follow-up guidance needed

## Recommended Sources

| Source                                                                                                                                                     | Type                                       | Artifacts Supported                                       | Why We'd Use It                                                                               | Notes / Gaps                                                                |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| [Synthea](https://synthetichealth.github.io/synthea/)                                                                                                      | Synthetic patient and encounter generator  | `MEDICAL_EVIDENCE`, `UNDERWRITING_CASE_NOTES`             | Strong open source base for medically grounded synthetic records and patient histories        | Not insurance-specific; needs adaptation into underwriting-facing artifacts |
| [Synthea Coherent Data Set](https://registry.opendata.aws/synthea-coherent-data/)                                                                          | Large linked synthetic healthcare dataset  | `MEDICAL_EVIDENCE`, `UNDERWRITING_CASE_NOTES`             | Adds richer linked records and broader evidence context than raw Synthea runs alone           | Still healthcare-centric rather than life-insurance-native                  |
| [aws-samples/sample-genai-underwriting-workbench-demo](https://github.com/aws-samples/sample-genai-underwriting-workbench-demo)                            | Demo repository with underwriting fixtures | `APPLICATION_SUMMARY`                                     | Directly relevant to life underwriting demos and useful for sample submission-style artifacts | Narrow sample set rather than a general-purpose generator                   |
| [gcc-insurance-intelligence-lab/insurance-datasets-synthetic](https://huggingface.co/datasets/gcc-insurance-intelligence-lab/insurance-datasets-synthetic) | Synthetic insurance dataset collection     | `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`, `CUSTOMER_REQUEST` | Useful base for structured insurance records and claim-adjacent data                          | Not tailored specifically to life-insurance servicing flows                 |
| [bdr-ai-org/claims-synthetic-dataset](https://huggingface.co/datasets/bdr-ai-org/claims-synthetic-dataset)                                                 | Synthetic claims dataset                   | `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`, `CUSTOMER_REQUEST` | Helps ground claim packages and claim-related structured context                              | Coverage is claims-oriented and may need reshaping for intake UX            |
| [memgraph/insurance-fraud](https://github.com/memgraph/insurance-fraud)                                                                                    | Insurance graph demo and generator         | `POLICY_SUMMARY`, `CLAIM_INTAKE_FORM`, `CUSTOMER_REQUEST` | Useful optional source for richer entity relationships across people, policies, and claims    | Fraud-demo framing is less directly aligned to the current PoC              |
| [Microsoft Genalog](https://github.com/microsoft/genalog)                                                                                                  | Synthetic document rendering toolkit       | Scan or noisy variants of supported artifacts             | Helpful for turning clean synthetic text into OCR-style or degraded document fixtures         | It renders documents; it does not provide insurance semantics on its own    |

## Artifact Mapping

| Artifact ID                     | Primary source(s)                                                                                                                           | Recommendation                                                                                                                       |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `MEDICAL_EVIDENCE`              | `Synthea`, `Synthea Coherent Data Set`                                                                                                      | Use these as the base source for synthetic clinical evidence when underwriting or review workflows need richer supporting documents. |
| `UNDERWRITING_CASE_NOTES`       | `Synthea`, `Synthea Coherent Data Set`                                                                                                      | Derive concise underwriter-style summaries or notes from the clinical and encounter history.                                         |
| `APPLICATION_SUMMARY`           | `aws-samples/sample-genai-underwriting-workbench-demo`, optionally `Synthea`-derived fields                                                 | Use the AWS sample repo as the primary reference fixture, with Synthea fields added only if a broader applicant snapshot is needed.  |
| `POLICY_SUMMARY`                | `gcc-insurance-intelligence-lab/insurance-datasets-synthetic`, `bdr-ai-org/claims-synthetic-dataset`, optionally `memgraph/insurance-fraud` | Start from structured insurance datasets and keep Memgraph optional for relationship-heavy scenarios.                                |
| `CLAIM_INTAKE_FORM`             | `gcc-insurance-intelligence-lab/insurance-datasets-synthetic`, `bdr-ai-org/claims-synthetic-dataset`, optionally `memgraph/insurance-fraud` | Use synthetic claim records as the base and normalize them into a simpler intake form shape for the PoC.                             |
| `CUSTOMER_REQUEST`              | `gcc-insurance-intelligence-lab/insurance-datasets-synthetic`, `bdr-ai-org/claims-synthetic-dataset`, optionally `memgraph/insurance-fraud` | Use these datasets for request context, then adapt the records into portal-style or support-style request inputs.                    |
| `DEATH_CERTIFICATE`             | No strong open fake-data source identified                                                                                                  | Synthesize this artifact from a template plus Synthea-derived facts if the chosen workflow requires it.                              |
| `BENEFICIARY_RECORD`            | Weak coverage in the recommended open sources                                                                                               | Hand-author a small set of believable beneficiary records matched to policy summaries.                                               |
| `SERVICE_REQUEST_FORM`          | Weak coverage in the recommended open sources                                                                                               | Hand-author a small set of service-request fixtures for the selected workflow.                                                       |
| Scan or noisy document variants | `Microsoft Genalog`                                                                                                                         | Use Genalog only after the clean source artifacts exist and the demo benefits from OCR-like document inputs.                         |

## Recommended Baseline Stack

Use these first for the PoC:

- `Synthea`
- `Synthea Coherent Data Set`
- `aws-samples/sample-genai-underwriting-workbench-demo`
- `gcc-insurance-intelligence-lab/insurance-datasets-synthetic`
- `bdr-ai-org/claims-synthetic-dataset`
- `Microsoft Genalog`

Keep `memgraph/insurance-fraud` optional for scenarios that benefit from richer relationship or policy graphs.

## Out of Scope for Now

- No data pipeline implementation
- No schema normalization yet
- No generated fixture files yet
- No decision on storage format beyond documenting likely sources
