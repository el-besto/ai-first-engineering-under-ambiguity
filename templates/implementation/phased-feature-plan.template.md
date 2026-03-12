<!-- AGENT INSTRUCTION: You MUST read `templates/implementation/phased-feature-plan.template.README.md` before using this template to create a new phase plan. Do not alter the structure of this document or omit list items unnecessarily. -->
# [Scenario Name]: Phase X Implementation Plan

## Phase Summary

- **Scenario:** `<scenario_name>`
- **Phase Goal:** `<phase_goal>`
- **Status:** `<draft | awaiting_review | in_progress | completed>`

## Contract Inputs

This phase must adhere to the following established boundaries:

- **Workshop spec:** `<workshop_spec_path>`
- **Architecture decisions:** `<decision_document_path>`
- **Deferred hardening:** `<defer_register_path>`
- **Acceptance test boundary:** `<acceptance_test_path>`

## Out Of Scope

Explicitly what this phase will *not* accomplish:

- `<out_of_scope_item>`
- *(Add as many items as needed)*

## Target Production Surface

The minimum supporting surface required to satisfy this phase:

### New Files

- `<path>` - `<purpose>`
- *(Add as many files as needed)*

### Modified Files

- `<path>` - `<what_is_changing>`
- *(Add as many files as needed)*

## Assertions & Behavior Contracts

- `<assertion>`
- *(Add as many assertions as needed)*

## Deferred Items Touched (If Any)

| Deferred item | Current assumption used | Hardening still required |
|---------------|-------------------------|--------------------------|
| `<item>`      | `<assumption>`          | `<next_step>`            |

## Ordered Implementation Steps

Implement in this order:

1. `<step>`
2. *(Add as many steps as needed)*

## Verification Plan

Verify the completion of this phase with evidence that:

- Review `docs/patterns.md` against the implemented changes. If any rule or architectural pattern is violated, halt and prompt the user to decide on resolution versus explicit waiver.
- Verify the observability posture: Ensure all new components bind `structlog` context correctly (component and operation-level), error paths use `log_exception`, and no raw PII, full claim documents, or raw prompts are exposed in logs.
- `<verification_step>`
- *(Add as many verification steps as needed)*

## Assumptions

- `<assumption>`
- *(Add as many assumptions as needed)*
