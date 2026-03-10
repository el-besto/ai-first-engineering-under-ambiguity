# [Scenario Name]: Slice Change Report

## Slice Summary

- Scenario: `<scenario_name>`
- Slice goal: `<slice_goal>`
- Primary user: `<primary_user>`
- Implementation status: `<status>`

## Contract Inputs

- Workshop spec: `<workshop_spec_path>`
- Deferred hardening: `<defer_register_path>`
- Tree A code map: `<tree_a_code_map_path>`
- Tree A worked example: `<tree_a_worked_example_path>`
- Acceptance test path: `<acceptance_test_path>`

## Acceptance Contract Status

| Area                         | Status     | Notes     |
|------------------------------|------------|-----------|
| Representative cases covered | `<status>` | `<notes>` |
| Acceptance fixtures present  | `<status>` | `<notes>` |
| Acceptance tests passing     | `<status>` | `<notes>` |
| Fakes in place               | `<status>` | `<notes>` |
| CI coverage                  | `<status>` | `<notes>` |

## Core Files Changed

### Acceptance contract

- `<path>` - `<why_it_matters>`

### Workflow facade / orchestration

- `<path>` - `<why_it_matters>`

### Entities / value objects

- `<path>` - `<why_it_matters>`

### Use cases

- `<path>` - `<why_it_matters>`

### Fake adapters

- `<path>` - `<why_it_matters>`

### Drivers / UI

- `<path>` - `<why_it_matters>`

### Tooling / Makefile / CI

- `<path>` - `<why_it_matters>`

## Execution Flows Touched

| Flow                         | What changed | Why it changed | Contract assertion | Files     |
|------------------------------|--------------|----------------|--------------------|-----------|
| Intake -> normalization      | `<summary>`  | `<reason>`     | `<assertion>`      | `<paths>` |
| Context assembly             | `<summary>`  | `<reason>`     | `<assertion>`      | `<paths>` |
| PII boundary                 | `<summary>`  | `<reason>`     | `<assertion>`      | `<paths>` |
| Completeness / ambiguity     | `<summary>`  | `<reason>`     | `<assertion>`      | `<paths>` |
| Reviewability / confidence   | `<summary>`  | `<reason>`     | `<assertion>`      | `<paths>` |
| Disposition selection        | `<summary>`  | `<reason>`     | `<assertion>`      | `<paths>` |
| Artifact generation          | `<summary>`  | `<reason>`     | `<assertion>`      | `<paths>` |
| Presentation / queue handoff | `<summary>`  | `<reason>`     | `<assertion>`      | `<paths>` |

## Fixtures / Tests Added Or Changed

- `<path>` - `<coverage>`

## Fakes Added Or Changed

- `<path>` - `<modeled_behavior>`

## Deferred Items Touched

| Deferred item | Impact on this slice | Current assumption used | Hardening still required |
|---------------|----------------------|-------------------------|--------------------------|
| `<item>`      | `<impact>`           | `<assumption>`          | `<next_step>`            |

## Runtime / Tooling Changes

- Runtime entrypoint(s): `<paths_or_commands>`
- Make targets added or changed: `<make_targets>`
- Framework wiring changed: `<summary>`
- Local dev or debug flow changed: `<summary>`
- CI command(s) added or changed: `<ci_command>`

## Reviewer Focus Areas

- `<focus_area_1>`
- `<focus_area_2>`
- `<focus_area_3>`

## Evidence

- Commands run: `<commands>`
- Test result summary: `<summary>`
- Demo path exercised: `<summary>`
- Trace/log evidence: `<path_or_note>`

## Follow-up Work

- `<required_next_work>`
- `<optional_hardening>`
- `<optional_polish>`
