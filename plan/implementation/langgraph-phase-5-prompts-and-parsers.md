# Death Claim Triage: Phase 5 Implementation Plan (Prompts & Parsers)

## Phase Summary

- **Scenario:** Death Claim Triage (Tree A)
- **Phase Goal:** Implement robust prompt templates and output parsers, then wire them directly into the graph nodes to replace fake text generation with actual LLM intelligence.
- **Status:** ready

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `plan/death-claim/workshop-spec.md`
- **Architecture decisions:** `plan/decisions/_langgraph-architecture-decisions.md` (Decision 3 - Generation Only)
- **Deferred hardening:** `plan/death-claim/deferred-hardening.md`
- **Acceptance test boundary:** `tests/acceptance/features/test_death_claim_intake_triage.py`

## Out Of Scope

- Granular use case files (`generate_case_summary_uc.py`, etc.). As agreed in the Attack Plan, we will consolidate the logic to avoid Clean Architecture boilerplate and wire the prompts directly into the LangGraph nodes.
- Secondary safety validation nodes (`claimant_message_policy.py`). We will rely on strong system instructions within the prompt templates to enforce empathetic tone and no-adjudication rules.

## Target Production Surface

### New Files

- `app/adapters/model/prompts/case_summary_prompt_template.py`
- `app/adapters/model/prompts/requirements_checklist_prompt_template.py`
- `app/adapters/model/prompts/follow_up_message_prompt_template.py`
- `app/adapters/model/prompts/routing_rationale_prompt_template.py`
- `app/adapters/model/parsers/case_summary_parser.py`
- `app/adapters/model/parsers/checklist_parser.py`
- `app/adapters/model/parsers/follow_up_message_parser.py`
- `app/adapters/model/parsers/routing_rationale_parser.py`

### Modified Files

- `app/interface_adapters/orchestrators/nodes/generate_artifacts_node.py` - Update to utilize the real prompt templates and parsers instead of returning hardcoded strings from the fake adapter.

## Assertions & Behavior Contracts

- The LLM must output clean, structured data (JSON or distinct artifact sections) that can be parsed by the output parsers.
- Prompts must include strict system instructions: DO NOT adjudicate the claim, DO NOT imply benefit determination, and USE an empathetic operational tone.
- The `generate_artifacts_node` must coordinate these prompt executions using the `LiveChatModelAdapter` implemented in Phase 4.

## Deferred Items Touched (If Any)

| Deferred item  | Current assumption used                   | Hardening still required                  |
|----------------|-------------------------------------------|-------------------------------------------|
| LLM Generation | Prompts handle safety instructions inline | External evaluation of LLM output quality |

## Ordered Implementation Steps

Implement in this order:

1. Create the 4 output parsers (Pydantic models / LangChain formatters) to enforce structured LLM generation.
2. Create the 4 prompt templates, ensuring they incorporate the required context (Policy, Intake Form, missing items) and enforce the guardrails (no adjudication, empathetic tone).
3. Modify `generate_artifacts_node.py` to assemble the context from `TriageGraphState`, execute the sequence of prompts via the configured `ModelAdapter`, parse the results, and update the state.
4. Verify the outputs against the 3 canonical cases locally.

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- The 3 acceptance fixtures pass locally, generating valid string artifacts in the `TriageGraphState` output.

## Assumptions

- We are relying on OpenAI formatted prompt templates and LangChain output parsers for execution compatibility.
