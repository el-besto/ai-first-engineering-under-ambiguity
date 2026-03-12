# Templates

This directory holds **reusable templates**, not live working documents.

Use it when you want to:

- start a new implementation-control document from a known shape
- start a new decision record from a known shape
- keep repeated scaffolding out of `plan/`

Directory split:

- `templates/decision/`
  - reusable decision-document templates
- `templates/implementation/`
  - reusable implementation templates
  - `acceptance-contract-plan.template.md` for fixture-driven PoC behavior work
  - `repo-bootstrap-plan.template.md` for setup, scaffold, and local runtime bootstrap
  - `tooling-validation-plan.template.md` for guardrail, runtime, and validation passes
- `plan/decisions/`
  - live filled-in decision records for this repo
- `plan/death-claim/`
  - source-of-truth scenario and design inputs
- `plan/implementation/`
  - live filled-in implementation-control documents for this repo

Rule of thumb:

- if the file is a reusable blank or parameterized starting point, it belongs here
- if the file is the current filled-in plan or report for this PoC, it belongs in `plan/implementation/`
- if the repo has distinct implementation doc types, prefer one targeted template per doc type instead of a generic implementation-plan template
