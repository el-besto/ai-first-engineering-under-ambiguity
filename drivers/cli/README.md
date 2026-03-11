# Bestow Developer CLI

This directory contains the `cli` driver for the Bestow backend. It is built using [Typer](https://typer.tiangolo.com/) and provides a unified interface for health checks, environment diagnostics, LLM integrations, and LangGraph workflow tooling.

**Usage:** Always execute the CLI from the project root.

```bash
./cli --help
```

---

## Command Reference

| Namespace | Command  | Description                                                                   |
|:----------|:---------|:------------------------------------------------------------------------------|
| `health`  | `deps`   | Check required local system binaries (Docker, Tilt, uv) and `.env`.           |
| `health`  | `api`    | Ping the local FastAPI ingress to ensure it is healthy.                       |
| `infra`   | `status` | List running Docker containers associated with the project.                   |
| `infra`   | `clean`  | Tear down local infrastructure running under `tilt`.                          |
| `llm`     | `quota`  | Check API key quota boundaries for the configured OpenAI organization.        |
| `llm`     | `ping`   | Measure the latency to the `gpt-4o-mini` chat completion endpoint.            |
| `graph`   | `run`    | Execute the Triage StateGraph locally against a predefined fake scenario.     |
| `graph`   | `trace`  | Generate and export a `.png` topology diagram of the current LangGraph state. |

---

## Copy-Paste Examples

### 🩺 Health Checks

Verify your local path dependencies and environment configuration:

```bash
./cli health deps
```

Ping the default local `.env` API or a specific target URL:

```bash
./cli health api
# Or
./cli health api --url "http://127.0.0.1:8000/health"
```

### 🐳 Infrastructure Settings

See if the `bestow` containers are successfully running in Docker:

```bash
./cli infra status
```

Destroy the currently running local cluster entirely:

```bash
./cli infra clean
```

### 🧠 LLM Usage & Connectivity

Check if your API connection is fast and healthy:

```bash
./cli llm ping
```

Make sure you haven't burned through your OpenAI credits for the active organization:

```bash
./cli llm quota
```

### 🕸️ LangGraph Inspection

Run the core Triage Graph workflow locally in memory against an instantiated set of Fakes representing a specific initial `ClaimIntakeBundle` scenario:

```bash
./cli graph run COMPLETE
./cli graph run MISSING
./cli graph run AMBIGUOUS
```

Automatically render a `.png` visualization of the actual compiled Node / Edge architecture inside the project's codebase:

```bash
./cli graph trace
```
