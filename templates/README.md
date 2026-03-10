# Templates

This directory holds **reusable templates**, not live working documents.

Use it when you want to:

- start a new implementation-control document from a known shape
- produce reviewer-friendly reports after an autonomous or semi-autonomous implementation pass
- keep repeated scaffolding out of `plan/`

Directory split:

- `templates/implementation/`
  - reusable implementation templates
- `plan/death-claim/`
  - source-of-truth scenario and design inputs
- `plan/implementation/`
  - live filled-in implementation-control documents for this repo

Rule of thumb:

- if the file is a reusable blank or parameterized starting point, it belongs here
- if the file is the current filled-in plan or report for this PoC, it belongs in `plan/implementation/`
