# Death-Claim: Repo Bootstrap Plan

## Summary

Use this document for the one-time bootstrap work that establishes the smallest runnable local baseline for the death-claim PoC.

This document owns scaffold, tooling, local runtime, and privacy-seam setup. It does **not** own fixture-driven PoC behavior implementation; that remains in [acceptance-contract-plan.md](./acceptance-contract-plan.md).

## Current Source Inputs

- Root tracker: [../../PROJECT_PLAN.md](../../PROJECT_PLAN.md)
- Slice anchor: [../death-claim/steel-thread.md](../death-claim/steel-thread.md)
- Tree A code map: [../death-claim/tree-a-code-map.md](../death-claim/tree-a-code-map.md)
- Repo patterns: [../../docs/patterns.md](../../docs/patterns.md)

## Bootstrap Scope

Create the smallest runnable baseline for:

- `pyproject.toml`
- `uv`
- Ruff
- Pyright
- `.env.example`
- `langgraph.json`
- minimal app, driver, and test folders

Add thin local delivery scaffolding for:

- Streamlit workbench shell
- FastAPI shell with `GET /health` and `POST /triage`
- single app `Dockerfile`
- `deploy/local/compose.yaml`
- `Tiltfile`

Add VS Code workspace bootstrap:

- `.vscode/extensions.json`
- `.vscode/settings.json`
- `.vscode/launch.json`

## Out Of Scope

This document does not own:

- fixture creation or acceptance-case truth
- workflow behavior, routing logic, or graph-step implementation
- live external LLM integration beyond the explicit privacy seam contract
- broader platform structure, persistence, workers, or non-local deployment work
- demo rehearsal, presentation assets, or broader validation posture

## Local Runtime Defaults

LangGraph local development defaults:

- primary dev loop: `langgraph dev`
- debug loop: `langgraph dev --debug-port 5678`
- initial tracing posture: `LANGSMITH_TRACING=false`

Standardized `Makefile` targets should include:

- `make install`
- `make dev`
- `make debug`
- `make api`
- `make ui`
- `make test`
- `make tilt`
- `make up`

## Privacy Seam Bootstrap

Define one explicit provider-agnostic privacy boundary before any external model call:

- contract name: `PIIGuardrailAdapter` or equivalent
- raw input in
- tokenized safe text and safe context out
- reversible token map out

Planned implementations behind the same contract:

- deterministic baseline implementation for the core slice
- stretch implementation using DSPy plus a local SLM runner such as Ollama or LM Studio

The local SLM path is not part of the critical path for the first working demo.

## Ordered Implementation Steps

1. Inspect the current repo first and extend existing files or structure instead of recreating them.
2. Establish the Python project baseline with `pyproject.toml`, `uv`, Ruff, Pyright, `.env.example`, and `langgraph.json`.
3. Add only the minimum app, driver, and test folder scaffold needed for the current death-claim slice.
4. Add the `Makefile` targets that support install, local graph development, debugging, API/UI shells, test execution, and local runtime helpers.
5. Add thin Streamlit and FastAPI shells, keeping Streamlit as the primary demo UI and FastAPI as a thin ingress over the same future graph-owned path.
6. Add the thinnest viable local runtime and deploy scaffold with a single app `Dockerfile`, `deploy/local/compose.yaml`, and `Tiltfile`.
7. Add the VS Code workspace bootstrap and ensure the debugger path lines up with `langgraph dev --debug-port 5678`.
8. Define the explicit `PIIGuardrailAdapter` seam or equivalent contract as bootstrap structure only, without implementing the broader workflow or live-model path in this pass.

## Tooling Defaults

Recommended VS Code extensions:

- `charliermarsh.ruff`
- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-python.debugpy`
- `tamasfe.even-better-toml`
- `redhat.vscode-yaml`
- `ms-azuretools.vscode-docker`
- `yzhang.markdown-all-in-one`
- `streetsidesoftware.code-spell-checker`

Recommended workspace settings:

- Ruff as the default Python formatter
- format on save for Python and Markdown
- Ruff fix-all and import organization on save
- workspace analysis enabled
- basic Markdown, YAML, and TOML validation enabled

## Bootstrap Done Criteria

Bootstrap is complete when:

- the repo has a runnable local scaffold
- thin baseline tooling is in place
- the LangGraph Studio development loop can start locally
- the VS Code debugger attach path is ready for use
- the privacy seam is explicit before any live external LLM integration

## Verification

Verify the bootstrap pass with the smallest practical checks:

- confirm the new baseline files and folders exist and are internally consistent
- run the repo formatting or lint checks that apply to the files you changed
- run `make install` or the equivalent bootstrap install path that lands in the repo
- start the local LangGraph development loop and confirm the baseline config is wired
- start the FastAPI shell and Streamlit shell and confirm both boot as thin stubs
- confirm the debugger configuration targets `langgraph dev --debug-port 5678`
- confirm the privacy seam is explicit in code structure before any live external model wiring exists

## Completion Report

Report the following at the end of a bootstrap pass:

- changed files
- which bootstrap scope items were completed
- checks run and their results
- any bootstrap gaps intentionally deferred
- any existing repo structure you reused instead of recreating
- anything that still blocks the acceptance-contract implementation pass

## Assumptions

- this document owns setup/bootstrap only, not fixture truth or PoC behavior
- broader platform structure is optional and should not be introduced unless it clearly strengthens the current slice
- Streamlit remains the primary demo UI
- FastAPI remains a thin ingress over the same graph-owned path
