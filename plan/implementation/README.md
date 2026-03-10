# Implementation Control

This directory holds the **live implementation-control documents** for the current PoC.

Working split:

- `plan/death-claim/`
  - defines what the slice must do
  - source-of-truth scenario and design inputs
- `plan/implementation/`
  - tracks how the current implementation pass is turning that into code
- `templates/implementation/`
  - reusable scaffolding for future implementation passes

Current implementation order:

1. fixtures
2. acceptance test
3. workflow facade / orchestration
4. entities and use cases
5. fake adapters
6. UI
7. tooling / Make targets

Current live documents:

- `acceptance-contract-plan.md`
- `change-reports/`

Use `change-reports/` for substantial autonomous or semi-autonomous implementation passes after code starts landing.
