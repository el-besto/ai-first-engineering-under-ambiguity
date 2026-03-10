# Implementation Control

This directory holds the **live implementation-control documents** for the current PoC.

Working split:

- [`../../PROJECT_PLAN.md`](../../PROJECT_PLAN.md)
  - repo-level assignment framing, deliverables, and progress
- `plan/death-claim/`
  - defines what the slice must do
  - source-of-truth scenario and design inputs
- `plan/implementation/`
  - tracks how the current implementation pass is turning that into code
  - separates one-time setup/bootstrap from the acceptance-driven PoC code path
- `templates/implementation/`
  - reusable scaffolding for future implementation passes

Current implementation order:

1. repo bootstrap and local scaffold
2. fixture contract and acceptance path
3. workflow facade / orchestration
4. entities, use cases, and fake adapters
5. UI and API surfaces
6. tooling and local validation

Current live documents:

- `repo-bootstrap-plan.md`
  - scaffold, tooling, local runtime, and privacy-seam bootstrap
- `tooling-validation-plan.md`
  - validation posture for tooling, guardrails, and thin local runtime checks
- `acceptance-contract-plan.md`
  - fixture-driven PoC code-path implementation plan
- `change-reports/`

Use `change-reports/` for substantial autonomous or semi-autonomous implementation passes after code starts landing.
