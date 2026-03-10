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

## Assumptions

- this document owns setup/bootstrap only, not fixture truth or PoC behavior
- broader platform structure is optional and should not be introduced unless it clearly strengthens the current slice
- Streamlit remains the primary demo UI
- FastAPI remains a thin ingress over the same graph-owned path
