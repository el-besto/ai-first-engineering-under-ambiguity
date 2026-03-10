# [Scenario Name]: Acceptance Contract Plan

## Summary

Use the current scenario/design docs as the primary contract and define the first real runnable acceptance test as a **workflow-facade test** backed by **filesystem fixture bundles**.

Chosen defaults:

- scenario: `<scenario_name>`
- scenario slug: `<scenario_slug>`
- test target: `<workflow_entrypoint>`
- fixture root: `<fixture_root>`
- acceptance test path: `<acceptance_test_path>`
- fake collaborators: `<fake_collaborators>`

## Current Source Inputs

- Workshop spec: `<workshop_spec_path>`
- Deferred hardening: `<defer_register_path>`
- Tree A code map: `<tree_a_code_map_path>`
- Tree A worked example: `<tree_a_worked_example_path>`
- Slice anchor: `<slice_anchor_path>`

## Acceptance-Contract Files To Create

- `<acceptance_test_path>`
- `<fixture_root>/case_a_<case_a_slug>/`
- `<fixture_root>/case_b_<case_b_slug>/`
- `<fixture_root>/case_c_<case_c_slug>/`
- `tests/acceptance/conftest.py`

## Fixture Bundle Expectations

Each representative case bundle should define:

- input artifacts present in the bundle
- expected disposition
- expected artifact outputs
- expected `<confidence_band>` or equivalent bounded confidence signal
- expected reviewability or escalation outputs
- expected summary of why the case took that path
- expected privacy assertions or tokenization outcomes

Fixture authoring rules:

- keep fixtures tiny, hand-authored, readable, and deterministic
- use the fixtures as the canonical acceptance fixtures immediately
- do not introduce a synthetic-data pipeline before the thin slice is stable

## Top-Level Test Boundary

The runnable acceptance test should target:

- `<workflow_entrypoint>`

The acceptance boundary should hide whether the implementation is:

- a direct orchestrator call
- a LangGraph-backed workflow
- a thin service object over Tree A use cases

## Out Of Scope

This document does not own:

- repo bootstrap or local scaffold setup beyond what is needed for the acceptance path
- broader runtime and tooling validation outside the acceptance-driving slice
- non-representative fixture libraries or synthetic-data expansion
- broader platform structure not required to satisfy the contract

## Minimal Supporting Production Surface

Only the minimum supporting surface required to satisfy the acceptance contract should exist:

- input/result objects:
  - `<domain_input_type>`
  - `<domain_result_type>`
  - `<assessment_types>`
- workflow owner that can:
  - `<step_1>`
  - `<step_2>`
  - `<step_3>`
  - `<step_4>`
  - `<step_5>`
  - `<step_6>`
- fake collaborators for:
  - `<fake_collaborator_1>`
  - `<fake_collaborator_2>`
  - `<fake_collaborator_3>`
  - `<fake_collaborator_4>`

## Assertions To Keep

- `<assertion_group_1>`
- `<assertion_group_2>`
- `<assertion_group_3>`
- `<assertion_group_4>`

## Assertions Intentionally Weakened Because Of Deferred Hardening

- `<weakened_assertion_1>`
  - reason: `<reason>`
- `<weakened_assertion_2>`
  - reason: `<reason>`

## Ordered Implementation Steps

Implement in this order:

1. create the fixture directories and representative case bundles
2. add fixture loaders that hydrate domain inputs from those files
3. add fake collaborator fixtures
4. write the acceptance test module
5. make the test run under the repo's async pytest setup
6. fill in only the minimum Tree A implementation needed to satisfy the contract

Acceptance scenarios that must pass:

- Case A -> `<disposition_a>`
- Case B -> `<disposition_b>`
- Case C -> `<disposition_c>`

## Verification

Verify the acceptance pass with evidence that:

- all representative cases pass through `<workflow_entrypoint>`
- the expected dispositions and bounded outputs are asserted for each case
- fake collaborators remain deterministic and stable across repeated runs
- privacy assertions are explicit for the model-facing path
- only the minimum production surface required by the contract was introduced

## Completion Report

Report the following at the end of an acceptance-contract pass:

- changed files
- fixtures created or changed
- tests run and their results
- fake collaborators introduced or updated
- any deferred hardening assumptions relied on
- anything still blocking the next implementation pass

## Assumptions

- the workshop spec remains the upstream behavior source
- the Tree A code map is sufficient as the naming and boundary map
- the first real acceptance test should stay framework-agnostic even if runtime implementation is framework-backed
- exact assertions tied to deferred hardening items should not be over-specified in v1
