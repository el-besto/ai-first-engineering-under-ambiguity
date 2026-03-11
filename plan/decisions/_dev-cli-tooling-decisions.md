# 005 Dev CLI Tooling: Decisions Needed

> **Template Version:** 1.0 (2025-10-13)
>
> **Usage Instructions:** See `templates/decision/decision-document-template.README.md` for how to use this template and how it fits into the repo's decision-record workflow.
>
> **Related Template:** Use this document when a cross-cutting repo or implementation decision needs explicit options, rationale, and status tracking.

---

**Status:** 🚧 0 of 2 Resolved | 2 Awaiting Discussion

This document captures the key decisions for introducing a Developer CLI layer using Typer and Rich to standardise local tooling and validation tasks.

**Update:** Initiated during the Tooling Validation Plan phase to replace ad-hoc scripts with proper CLI commands. Added comprehensive namespace brainstorm and library evaluations based on user feedback.

---

## Decision 1: Scope and Structure of the Developer CLI

**Agent Analysis:**

- The current tooling (like `tools/check_openai_quota.py`) is written as a standalone script.
- As the PoC grows, we need consistent ways to run validations, check limits, run the LangGraph simulation locally, and potentially seed data.
- The user provided examples (`homelab-server`, `iac-terraform`, `career-map`) that all successfully leverage a nested `typer` application setup with `rich` for formatting.
- Other adjacent libraries observed in user examples:
  - `httpx` (async HTTP client)
  - `python-dotenv` (already in our `pyproject.toml`)
  - `pyyaml` (for parsing configs/fixtures)
  - `tabulate` (or we can just use `rich.table` which provides excellent tables)
  - `tenacity` (retry logic—highly valuable for wrapping flaky external LLM or API calls during automation/seeding)

**Context:**
We are actively executing the `tooling-validation-plan.md` and need a cleaner way to invoke backend tests, model evaluations, and system checks without relying solely on raw python scripts or expanding the Makefile endlessly. We don't necessarily need a massive CLI, but it should be structured to allow for quick developer tasks.

**Decision Required:**
How should we structure and deploy the CLI for `bestow-poc`?

- [ ] **Option A: Lightweight Drivers CLI (`drivers/cli`)**
  - Implement a slim Typer application inside `drivers/cli/main.py`.
  - Use namespaces for targeted developer commands (see Decision 2).
  - ✅ Pro: Treats the CLI as a first-class citizen using the same DI containers as the API and UI. Keeps "app" code decoupled.
  - ✅ Pro: Scales cleanly if we need to add synthetic data generation later.
  - ❌ Con: Slightly more boilerplate to set up initially than a flat script.

- [ ] **Option B: Flat Tools CLI (`tools/cli.py`)**
  - Keep the CLI explicitly in the `tools/` directory as a single entrypoint script holding Typer commands without sub-modules.
  - Command: `uv run python tools/cli.py check quota`.
  - ✅ Pro: Extremely fast to implement.
  - ❌ Con: Might get messy when we add complex database seeding or need access to domain entities.

**User Decision:** ✅ **Option A: Lightweight Drivers CLI (`drivers/cli`)**

**Rationale:**
Allows for continual improvement and keeps "app" code decoupled while sharing DI containers. Following principles of DRY and maintainability, command logic will be segmented by namespace into separate files, supported by a `utils/` directory to prevent massive file bloat and enable straightforward unit testing.

**Impact:** MEDIUM - Decides how local developers and automated scripts will interact with the application offline or in utility modes.

**Status:** ✅ RESOLVED

---

## Decision 2: Target CLI Namespaces & Commands

**Agent Analysis:**
To prevent building an overly massive CLI, we should intentionally select only the namespaces we strictly foresee needing for the `bestow-poc` Developer Experience and Tooling Validation plan.

Here is a comprehensive brainstorm of potential commands:

**1. `llm` (LLM & Provider Checks)**

- *Note: Since we will leverage both the main cloud LLM and a local SLM (Ollama), these commands should accept a `--target` flag (e.g. `--target main`, `--target guardrail`) to route the check accordingly.
- `cli llm quota`: Verify API key, display available models, and check remain limits.
- `cli llm ping`: Send a basic 1-token prompt to verify latency and model connection.

**2. `health` (System Diagnostics)**

- `cli health api`: Ping the local FastAPI `GET /health` to ensure it's alive.
- `cli health deps`: Verify the environment `.env` file is fully valid and dependencies are linked.

**3. `graph` (LangGraph Workflows)**

- `cli graph run [fixture_name]`: Execute the graph head-less (without Streamlit/API) using a fixture, useful for debugging the state directly in the terminal.
- `cli graph trace`: Generate or dump the current LangGraph Mermaid output.

**4. `data` (Synthetic Generation & Fixtures)**

- `cli data seed-fixtures`: Generate synthetic death claim forms, obituaries, etc., using the main LLM and save them to `tests/acceptance/fixtures/`.
- `cli data validate`: Read existing fixtures and run a quick schema validation against them.

**5. `infra` (Local Environment)**

- `cli infra status`: Check Docker/tilt status for the local stack.
- `cli infra clean`: Prune local state, temporary DB tables, or dangling containers.

**Library Evaluation: Tenacity vs. LangChain Backoff:**

- **LangChain Built-in Retry:** For the actual LangGraph orchestration (the LLM nodes), we should rely on LangChain's built-in `.with_retry()` or constructor-level `max_retries`. LangChain's implementations are specifically designed to interpret provider-specific rate limit headers (like `429` retry-after logic).
- **Tenacity:** We should still adopt `tenacity` for the **CLI and System Tools**. It is highly valuable for broader orchestration tasks that LangChain doesn't cover. For example: polling until a local Ollama container is healthy during deployment, retrying database connections in future seed scripts, or wrapping E2E test endpoint calls to wait for FastAPI to boot.

**User Decision:** ✅ **Keep all proposed commands (`llm`, `health`, `graph`, `data`, `infra`)**

**Rationale:**
These commands are simple and highly targeted. They significantly improve the local testing loop. For the `data seed-fixtures` command, we will implement it as a pending stub returning a message such as "PENDING. Complete once the synthetic-data-plan has been executed." to adhere to iterative progression. We will also include `tenacity`, `httpx`, `pyyaml`, and `typer` (with `rich` formatting) as supporting tools for these system workflows.

**Impact:** MEDIUM

**Status:** ✅ RESOLVED

---

## Summary Of Decisions

| # | Decision                                 | Priority | Status     |
|---|------------------------------------------|----------|------------|
| 1 | Scope and Structure of the Developer CLI | MEDIUM   | ✅ RESOLVED |
| 2 | Target CLI Namespaces & Commands         | MEDIUM   | ✅ RESOLVED |

---

## Next Steps

**Completed:**

- ✅ Reviewed user-provided CLI examples from adjacent repositories.
- ✅ Drafted initial decision document outlining CLI positioning.
- ✅ Expanded to include namespace brainstorming and library evaluations (`tenacity`, `rich`, `httpx`).
- ✅ User reviewed and approved structural Option A and all proposed namespaces.

**Awaiting Input (0 decisions):**

*None*

**After Decisions Resolved:**

1. Install necessary dependencies (`uv add typer[all] httpx tenacity pyyaml`).
2. Scaffold `drivers/cli` with segmented commands (e.g., `commands/llm.py`, `utils/formatting.py`).
3. Port `tools/check_openai_quota.py` to the new CLI's `llm quota` command.
4. Add stub implementations for all other commands.
5. Provide a custom run wrapper or document CLI execution in Makefile.

**Status:** 2 of 2 decisions resolved | 0 awaiting collaborative review
