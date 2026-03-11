# Patterns & Conventions - bestow-poc

**Purpose:** Repo-wide v1 implementation policy for `bestow-poc`, grounded in the current death-claim steel thread and Lean-Clean Tree A baseline, and adopting Lean-Clean standards from `lean-clean-python-style-guide/AGENT_REFERENCE.md` except where repo-local code, tests, decisions, or deferred-hardening items narrow them.

**Maintenance Note:** This repo is still doc-first. When this document names paths under `app/`, `drivers/`, `deploy/`, or `tests/`, treat them as planned Tree A locations from `plan/death-claim/tree-a-code-map.md` unless the paths already exist in the repo.

**Related-Doc Precedence:** Follow the precedence rules in Section 1.4. For provisional hardening items, defer to `plan/death-claim/deferred-hardening.md` until those items are intentionally hardened.

---

## 1. Document Purpose & Usage

### 1.1 Purpose

`bestow-poc` uses this document to define the implementation patterns that all planned app code, tests, scripts, docs, and committed demo artifacts must follow.

### 1.2 Scope

This document applies to:

- planned production app code for the death-claim PoC
- tests and acceptance fixtures
- repo automation and support scripts
- repo-authored documentation and demo artifacts that describe or constrain the implementation

Out of scope:

- `.scratch/` planning notes except as temporary execution inputs
- local caches, editor state, virtual environments, and build artifacts

### 1.3 Audience

Primary audience:

- maintainers
- implementers
- reviewers
- AI coding agents

### 1.4 Source-of-Truth Precedence

Use this precedence order when multiple docs overlap:

1. Repo code, tests, and enforced config
2. Narrow repo docs:
   - `AGENT_RULES.md`
   - `PROJECT_PLAN.md`
   - `plan/decisions/_langgraph-architecture-decisions.md`
   - `plan/death-claim/workshop-spec.md`
   - `plan/death-claim/steel-thread.md`
   - `plan/implementation/README.md`
   - `plan/death-claim/tree-a-code-map.md`
   - `plan/death-claim/tree-a-worked-example.md`
3. Upstream Lean-Clean standards:
   - `../lean-clean-code/lean-clean-python-style-guide/AGENT_REFERENCE.md`
4. `docs/patterns.md`
5. Historical or execution-draft artifacts under `.scratch/`

Repo-specific exception:

- For rules marked provisional in this document, the active defer register is `plan/death-claim/deferred-hardening.md`.
- This file is a downstream adoption layer. It should pass Lean-Clean standards into `bestow-poc`, then record repo-local exceptions or narrower choices.

---

## 2. Agent Playbook

### 2.1 Objective

Keep `docs/patterns.md` accurate, minimal, and directly actionable for implementers and reviewers by passing Lean-Clean standards into this repo and documenting only the repo-local adoptions, exceptions, and deferments.

### 2.2 Inputs To Inspect

Inspect these sources before updating this document:

- `AGENT_RULES.md`
- `PROJECT_PLAN.md`
- `Makefile`
- `.pre-commit-config.yaml`
- `.markdownlint-cli2.yaml`
- `.editorconfig`
- `cspell.config.yaml`
- `../lean-clean-code/lean-clean-python-style-guide/AGENT_REFERENCE.md`
- `plan/decisions/_langgraph-architecture-decisions.md`
- `plan/implementation/README.md`
- `plan/death-claim/process-understanding.md`
- `plan/death-claim/workshop-spec.md`
- `plan/death-claim/steel-thread.md`
- `plan/death-claim/tree-a-code-map.md`
- `plan/death-claim/tree-a-worked-example.md`
- `plan/death-claim/deferred-hardening.md`

### 2.3 Fill Sequence

Fill or update the document in this order:

1. Purpose, scope, audience, and precedence
2. Non-negotiable architecture and guardrail rules
3. Core Tree A placement and boundary patterns
4. Cross-cutting conventions for typing, errors, tracing, and workflow hygiene
5. Testing, fixtures, examples, and anti-patterns
6. Change log and open gaps

### 2.4 Escalation Rules

Escalate instead of guessing when:

- a policy change would alter the public API or the bounded triage result shape
- a rule would move business logic out of use-cases or entities and into a graph, UI, or driver
- a change would relax the PII boundary or no-adjudication guardrails
- two repo docs conflict and current code does not resolve the conflict
- a provisional hardening item is about to become acceptance-driving behavior

### 2.5 Verification Checklist

Before finalizing an update, verify:

- every rule is grounded in repo code, enforced config, or the higher-precedence docs listed above
- planned Tree A paths are labeled as planned when the files do not yet exist
- provisional items still point back to `plan/death-claim/deferred-hardening.md`
- examples and anti-patterns still match the current v1 slice
- stale planning assumptions have not been carried forward as fact

### 2.6 Update Protocol

When updating this document:

1. Preserve valid repo policy
2. Rewrite sections that no longer match code or the active slice
3. Convert planned-path language into implemented-path language as code lands
4. Keep provisional hardening items explicit until they are deliberately closed
5. Add a dated change-log note for material updates

---

## 3. Non-Negotiable Rules

### 3.1 Review Checklist

Reviewers must confirm:

- [ ] Tree A layering is preserved and graph nodes stay thin wrappers around use-cases, ports, or adapter calls
- [ ] Use-cases depend only on domain types and adapter `protocol.py` contracts, never on concrete `fake.py`, provider implementations, or driver/framework types
- [ ] Tests cover the affected boundary: acceptance fixtures for triage behavior, unit checks for guardrails and pure policies, and smoke coverage for graph/API/UI paths as needed
- [ ] Raw PII never crosses the external model boundary, the PoC never implies adjudication or benefit determination, and human-review boundaries remain explicit
- [ ] Streamlit and FastAPI call the same graph-owned triage path and return one bounded disposition per run

### 3.2 Architectural Invariants

- Dependencies flow inward through the Tree A layers: `drivers -> interface_adapters -> use_cases -> adapter contracts/domain`.
- Domain logic must not depend on FastAPI, Streamlit, LangGraph runtime types, vendor SDKs, storage clients, prompt templates, or raw transport schemas.
- Cross-layer transformations happen in mappers, presenters, parsers, and adapter boundaries, not in entities or use-cases.
- LangGraph owns workflow runtime, but business rules stay in entities and use-cases (Lean-Clean `C8`).
- Graph state must not carry vendor clients, prompt templates, or persistence handles. Raw PII in graph state is a temporary deferred-hardening exception only where already documented; do not widen that exception, and always place a `tokenize_pii` boundary before any external model call (Lean-Clean `B8`, `C8`; repo-local exception via `plan/death-claim/deferred-hardening.md`).
- Every triage run ends in exactly one bounded disposition: `proceed`, `request_more_information`, or `escalate_to_human_review`.

### 3.3 Allowed Exceptions

- Driver dependency modules may construct concrete adapters, choose fake versus live implementations, and manage client lifecycle.
- Driver-edge request or response schemas may use framework-specific models, but they must be mapped inward immediately.
- Small adapter-local parsing schemas for structured LLM output are allowed if they remain outside the application core and are mapped immediately into internal types.
- Fake adapters are allowed for deterministic tests, local demo scaffolding, and early graph stabilization.

### 3.4 Definition Of Done

A change is not complete until:

- it follows the rules in this document or records an intentional exception in a higher-precedence doc
- required tests or manual validations for the affected boundary are present or explicitly waived
- any new reusable repo-wide pattern is documented here or in a narrower source-of-truth doc
- reviewers can trace the change to the correct Tree A layer

---

## 4. Core Architecture Patterns

### 4.1 Domain Model Patterns

- Primary domain model type: immutable Python dataclasses in planned `app/entities/`
- Mutability rule: immutable by default with `@dataclass(slots=True, frozen=True)`
- Validation rule: transport and payload shape validation happens at the driver edge; business invariants live in entity constructors/helpers and use-case policy
- Boundary rule: domain models must not import framework code, vendor SDKs, storage clients, prompt templates, or tracing libraries

Canonical planned v1 domain and result types:

- `ClaimIntakeBundle`
- `CompletenessAssessment`
- `AmbiguityAssessment`
- `ReviewabilityAssessment`
- `TriageDisposition`
- `TriageResult`

### 4.2 Use Case / Service Patterns

- Primary unit of orchestration: use-case modules or classes in planned `app/use_cases/`
- Input shape: typed request models or command-style dataclasses assembled once by a mapper, controller, or graph wrapper
- Output shape: typed domain results and artifact models, with `TriageResult` as the bounded end-state contract for the v1 flow
- Side-effect policy: all I/O is isolated behind adapter contracts in planned `app/adapters/*/protocol.py`

Rules for use-cases:

- Keep routing, completeness, ambiguity, reviewability, and no-adjudication policy out of the graph runtime
- Depend on adapter protocols only, never on concrete `fake.py` or provider implementations
- Return typed results that make ambiguity and escalation explicit instead of hiding those outcomes in exceptions

### 4.3 Repository Patterns

The v1 slice is fake-backed and in-memory by default, so the primary boundary is the adapter contract rather than a broad persistence layer.

- Interface location: planned `app/adapters/policy_lookup/protocol.py`, `app/adapters/document_intake/protocol.py`, `app/adapters/model/protocol.py`, `app/adapters/safety/protocol.py`, and `app/adapters/review_queue/protocol.py`
- Implementation location: planned `app/adapters/*/fake.py` for deterministic collaborators, plus planned provider or parser modules where live integrations are required
- Return type guidance: use concrete domain dataclasses for single operations and `Sequence[...]` for ordered collections; do not leak raw vendor payloads or ad hoc dict shapes across the boundary
- Conversion boundary: persistence, storage, or vendor payloads become typed domain entities or typed facts inside adapters and parsers before reaching use-cases or graph state

Broad `app/infrastructure/` concerns remain deferred unless the slice expands beyond the current steel thread.

### 4.4 Mapper Vs Presenter Patterns

- Mapper purpose: convert workbench and API input into internal request models and initial graph state once
- Presenter purpose: convert typed internal results into outbound UI or API views once and attach edge observability
- Anti-confusion rule: mappers do not format outbound views, and presenters do not decide dispositions or repair incomplete domain data

Planned Tree A mapper and presenter locations:

- `app/interface_adapters/mappers/workbench_request_mapper.py`
- `app/interface_adapters/mappers/api_request_mapper.py`
- `app/interface_adapters/mappers/response_mapper.py`
- `app/interface_adapters/presenters/triage_result_presenter.py`
- `app/interface_adapters/orchestrators/triage_graph_state.py`

### 4.5 Dependency Injection / Composition Root

- Composition root location: planned `drivers/api/dependencies.py` and planned `drivers/ui/streamlit/dependencies.py`
- Injection style: manual wiring from driver dependency modules into the graph, orchestrator, use-cases, and adapters
- Ownership rule: drivers and dependency modules create and close external clients; entities, use-cases, and graph state do not own client lifecycle
- LangGraph factory rule: compile graphs in a factory such as `build_triage_graph(adapters: AdapterRegistry)` and inject adapters through closures over a small registry object rather than through state or globals (Lean-Clean `B8`, `C8`; current repo decision in `plan/decisions/_langgraph-architecture-decisions.md`)
- Graph state rule: prefer a flat `TypedDict` accumulation state with simple values or known dataclasses; use `Annotated[..., operator.add]` reducers for append-only list fields and map back into `TriageResult` at the boundary (Lean-Clean `A2.1`, `B8`)
- Graph branching rule: conditional edges branch on typed disposition or other deterministic state, never on free-form model text (Lean-Clean `D3`)
- Current v1 topology preference: this repo currently favors phase-oriented nodes over one giant node, following the implementation-phase split of deterministic extraction and routing first, then privacy and artifact generation. This is a repo-local preference from `plan/decisions/_langgraph-architecture-decisions.md`, not a universal Lean-Clean rule.

Primary planned delivery entrypoints:

- Streamlit workbench under `drivers/ui/streamlit/`
- FastAPI `GET /health`
- FastAPI `POST /triage`

### 4.6 Configuration Management

- Primary config mechanism: small settings or dependency-wiring objects loaded from environment variables and local `.env` support at the driver/config layer
- Allowed direct env access: config and dependency wiring only, plus short-lived repo automation scripts
- Required defaults and override policy: default to fake-backed local operation, local-first tracing, and opt-in live provider credentials for the demo path

---

## 5. Cross-Cutting Conventions

### 5.1 Naming And Code Style

- Primary language: Python for the planned app slice, Markdown for repo docs and planning artifacts
- Naming conventions: snake_case for modules and functions, PascalCase for classes, `Literal` or `StrEnum` for bounded dispositions and confidence bands
- Formatting and linting tools:
  - current repo: `make format-md`, `tools/format-markdown.cjs`, `.markdownlint-cli2.yaml`, `pre-commit`, `cspell`
  - planned app baseline: `uv`, Ruff, and Pyright, consistent with `PROJECT_PLAN.md` and `plan/implementation/repo-bootstrap-plan.md`
- Type annotation policy: full annotations are required for app code, protocols, graph state, boundary DTOs, and tests that cross architectural boundaries

### 5.2 Logging

- Log using the app-configured logger from drivers, presenters, and adapters that touch I/O
- Technology baseline: `structlog` with request-scoped contextvars and `log_exception(...)` for consistent error fields
- Event naming rule: prefer short standard events like `started`, `completed`, and `failed`; add operation context through bound fields instead of verbose event names
- Required binding pattern:
  - bind component context once in `__init__` or module setup (`adapter=...`, `driver=...`, `orchestrator=...`, `node=...`)
  - bind `operation=...` at the start of each method or request handler and reuse the local bound logger
- Required context: case or bundle identifier, surface, selected disposition, confidence band, and reviewability state when that information is available
- Error logging rule: use `log_exception(log, "failed", exc, **context)` instead of ad hoc `logger.error(...)` or `logger.exception(...)`
- Privacy rule: do not log raw PII, policy numbers, full claim documents, raw prompts, raw model completions, token maps, secrets, or credentials
- Safe derived fields: prompt length, response length, document count, generated field names, adapter mode, and token counts
- Forbidden patterns: `print` in planned app code, raw prompt logging, raw PII logging, f-string log messages that hide fields, and silent guardrail failures

Example patterns:

**1. Request or session context binding**

```python
import uuid

from fastapi import Request

from app.infrastructure.telemetry.logger import (
    bind_context,
    clear_context,
    get_logger,
    log_exception,
)

logger = get_logger(__name__).bind(driver="FastAPI", surface="api")


async def correlation_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    clear_context()
    bind_context(
        request_id=request_id,
        path=request.url.path,
        method=request.method,
        surface="api",
    )
    log = logger.bind(operation="http_request")
    log.info("started")
    try:
        response = await call_next(request)
        log.info("completed", status_code=response.status_code)
        return response
    except Exception as exc:
        log_exception(log, "failed", exc)
        raise
    finally:
        clear_context()
```

**2. Component + operation binding**

```python
from app.infrastructure.telemetry.logger import get_logger, log_exception


class TriageOrchestrator:
    def __init__(self, ...):
        self.logger = get_logger(__name__).bind(
            orchestrator=self.__class__.__name__
        )

    async def assess(self, bundle: ClaimIntakeBundle) -> TriageResult:
        log = self.logger.bind(operation="assess", case_id=bundle.case_id)
        log.info("started", document_count=len(bundle.documents))
        try:
            ...
            log.info(
                "completed",
                selected_disposition=result.disposition,
                confidence_band=result.confidence_band,
                reviewability_state=(
                    "needs_review" if result.reviewability_flags else "clear"
                ),
            )
            return result
        except Exception as exc:
            log_exception(log, "failed", exc)
            raise
```

**3. Consistent error logging**

```python
from app.infrastructure.telemetry.logger import get_logger, log_exception

logger = get_logger(__name__).bind(route="/triage", surface="api")


def run_triage(graph: CompiledStateGraph, bundle: ClaimIntakeBundle):
    log = logger.bind(operation="run_triage", case_id=bundle.case_id)
    log.info("started")
    try:
        result = graph.invoke({"claim_bundle": bundle})
        triage_result = map_state_to_triage_result(result)
        log.info(
            "completed",
            selected_disposition=triage_result.disposition,
            confidence_band=triage_result.confidence_band,
            reviewability_state=(
                "needs_review" if triage_result.reviewability_flags else "clear"
            ),
        )
        return triage_result
    except Exception as exc:
        log_exception(log, "failed", exc)
        raise
```

**4. Safe model or guardrail logging**

```python
from app.infrastructure.telemetry.logger import get_logger, log_exception


class LiveChatModelAdapter:
    def __init__(self, model_name: str):
        self.logger = get_logger(__name__).bind(
            adapter=self.__class__.__name__,
            model_name=model_name,
        )

    def generate(self, prompt: str) -> str:
        log = self.logger.bind(operation="generate")
        log.info("started", prompt_chars=len(prompt))
        try:
            response = self.client.invoke(prompt)
            content = str(response.content)
            log.info("completed", response_chars=len(content))
            return content
        except Exception as exc:
            log_exception(log, "failed", exc, prompt_chars=len(prompt))
            raise


class VaultlessPIIGuardrail:
    def tokenize(self, raw_input: str) -> tuple[str, dict[str, Any]]:
        log = self.logger.bind(operation="tokenize")
        log.info("started", input_chars=len(raw_input))
        ...
        log.info("completed", token_count=len(token_map))
        return safe_input, token_map

# Log derived fields like prompt_chars, response_chars, input_chars, and token_count.
# Do not log raw prompts, policy numbers, raw PII, token maps, or full claim documents.
```

### 5.3 Error Handling

- Surface errors at the driver boundary
- Wrap or normalize errors using typed application or adapter errors before they reach UI or HTTP responses
- Re-raise vs absorb rule: inner layers re-raise typed errors; drivers and presenters translate them into bounded API, UI, or demo-safe failure modes
- Required logging or tracing on failure: record the failing step, adapter, and correlation context without raw PII, full claim documents, or raw prompts

Business ambiguity is not an exception path. It must be represented by typed triage results, reviewability flags, or escalation reasons.

### 5.4 Observability / Tracing

- Tracing approach: local-first graph inspection and replay, with initial posture `LANGSMITH_TRACING=false`
- Metrics approach: lightweight run visibility is sufficient for v1; a full metrics stack is deferred
- Instrumentation boundary: presenters, drivers, and thin graph wrappers add traces or run metadata; entities and use-cases remain free of tracing imports
- Request-scoped context rule: bind and clear request or session context at the driver entrypoints so all downstream logs carry the same correlation fields
- Trace correlation rule: when OpenTelemetry spans are present, include `trace_id` and `span_id` automatically; absence of OpenTelemetry must not break logging
- Do-not-log or do-not-trace rule: raw PII, full raw claim documents, reversible token maps, raw prompts, secrets, and provider credentials

---

## 6. Infrastructure & Integration Patterns

### 6.1 Client Lifecycle

- Client config type: config or settings objects passed from dependency modules
- Lifecycle policy: startup or shutdown hooks for API clients, session-scoped helpers for Streamlit as needed, and simple process-local fakes for tests or local demos
- Ownership rule: drivers and dependency modules close live clients

### 6.2 Persistence Conventions

- Persistence technology: none in v1 beyond in-memory fakes, local acceptance fixtures, and transient graph runtime state
- Persistence model rule: if storage is added later, persistence models stay in adapters or infrastructure and map inward immediately
- Query or session rule: not applicable in v1; do not add ad hoc storage access from use-cases or graph nodes
- Migration rule: deferred until the repo adopts a real store

### 6.3 Vendor Isolation

- Vendor SDKs are allowed in adapters and future infrastructure only
- Vendor response normalization occurs in gateway, parser, or adapter modules before data reaches entities, use-cases, presenters, or graph state
- Domain and application layers must not depend on FastAPI, Streamlit, LangGraph runtime types, OpenAI or other model SDKs, database clients, or raw vendor payload dicts

---

## 7. Optional Extensions

### 7.1 AI / LLM Patterns

Use this section to record how `bestow-poc` adopts Lean-Clean LLM, LangGraph, and future DSPy standards from `../lean-clean-code/lean-clean-python-style-guide/AGENT_REFERENCE.md`.

#### 7.1.1 LangGraph Workflow Shape

- Graph orchestration location: LangGraph factories and node wrappers live in `app/interface_adapters/orchestrators/`; nodes stay thin and delegate to use-cases or adapter-backed helpers (Lean-Clean `C8`, `B8`)
- Graph state pattern: use a flat `TypedDict` for accumulation, keep reducers explicit, and provide a dedicated mapper from graph state to `TriageResult` (Lean-Clean `A2.1`, `B8`)
- This repo currently uses `StateGraph` rather than `create_agent` because the workflow has explicit state, branching, and future privacy/HITL steps (Lean-Clean `B7`, `C8`; repo-local decision in `plan/decisions/_langgraph-architecture-decisions.md`)
- Repo-local v1 topology preference: keep the workflow phase-oriented and legible. Current preferred shape is deterministic extraction and triage first, then `tokenize_pii`, then disposition-specific artifact generation (`D3` for deterministic routing; repo-local topology choice from `plan/decisions/_langgraph-architecture-decisions.md`)
- Conditional routing rule: branch on deterministic state such as `disposition`, not on unstructured model output (Lean-Clean `D3`)

#### 7.1.2 Model Adapters, Structured Output, and Prompt Boundaries

- Prompt or signature location: planned `app/adapters/model/prompts/`, with parsers in planned `app/adapters/model/parsers/` and live providers in planned `app/adapters/model/providers/`
- Boundary rule: Models and prompts must stay completely out of domain entities, use-cases, and graph state (Lean-Clean `Golden Rule 6`, `C8`)
- Structured output rule: use explicit parsers or small adapter-local Pydantic schemas and map immediately into internal dataclass types. Never import Pydantic into the domain (Lean-Clean `B9`, `C3`, `Golden Rule 3`)
- LLM payload rule: Build `openai_payload` strings/dicts only at the gateway boundaries. Do not merge `**kwargs` strings inside use-cases or graph nodes (Lean-Clean `B1`, `Golden Rule 1`)
- Provider injection rule: live provider adapters are opt-in via dependency wiring and environment configuration; tests and default local runs keep a fake adapter path available (Lean-Clean `C4`, `C8`; repo-local live-wiring plan in `plan/implementation/langgraph-phase-4-live-model-wiring.md`)
- Fake-vs-live rule: preserve the same protocol boundary for fake and live model adapters so acceptance tests, Streamlit, and FastAPI do not fork behavior (Lean-Clean `C4`, `A7`)

#### 7.1.3 Evaluation And Validation

- Evaluation and observability rule: keep a fake model adapter for deterministic tests, but validate the demo path with live provider-backed runs across the representative cases or dispositions (Lean-Clean `D8`, `B12`; repo-local live validation plan in `plan/implementation/langgraph-phase-4-live-model-wiring.md`)

#### 7.1.4 DSPy And Local SLM

- DSPy rule: if DSPy is introduced, keep it feature-local and adapter-facing, behind the same protocol boundaries as any other model integration. Do not use DSPy to replace deterministic triage routing or policy enforcement (Lean-Clean `B14`, `C8`, `D3`)
- Signature Design rule: Treat DSPy Signatures as comprehensive instruction sets, not just I/O contracts. Include a Role Definition, Goal Statement, Process Steps, and Decision Rules in the signature docstring (Elysia Pattern 1).
- Typed Output rule: Use DSPy typed `OutputField` with Pydantic models for automatic JSON → object parsing at the adapter boundary. Do not manually parse JSON dicts (DSPy Reference).
- Reasoning Fields rule: Include a `reasoning: str` OutputField to ensure LLM transparency and chain-of-thought before it generates the final disposition or artifacts (Elysia Pattern 4).
- Stretch-path rule: DSPy or local SLM work is confined to the privacy seam and must remain swappable behind `PIIGuardrailAdapter` (repo-local stretch path, not a universal Lean-Clean requirement)

#### 7.1.5 Prompt Engineering (Elysia Patterns)

If writing raw prompts or DSPy Signatures, apply these Elysia production patterns:

- **Comprehensive Context:** Define the persona, goal, and step-by-step reasoning process directly in the prompt/signature docstring.
- **Detailed Field Descriptions:** Provide extensive `desc=` kwargs for DSPy fields. Show concrete formats, edge cases (e.g., "If no result, return empty list []"), and constraints.
- **Explicit "Do NOT" rules:** List known failure modes or anti-patterns explicitly in the prompt (e.g., "Do NOT create generic roles like 'Role 1'").
- **Multi-Output Fields:** Break complex generation tasks into multiple distinct OutputFields rather than asking for one massive JSON blob.
- **Input Context:** Use `InputField` descriptions to explain *how* the LLM should use the input data, not just what it is.

### 7.2 API-Specific Patterns

- Request validation location: planned `drivers/api/schemas/` and planned `app/interface_adapters/mappers/api_request_mapper.py`
- Response and presenter rule: `POST /triage` validates the request once, maps inward once, invokes the shared graph-owned triage path, and returns a presenter-shaped bounded response; `GET /health` stays thin and non-domain
- Error envelope rule: driver code translates typed app errors into HTTP responses; streaming-specific rules are deferred until streaming exists
- Versioning or compatibility rule: internal v1 API only; keep the contract small and aligned with the workbench path

### 7.3 UI / Streamlit Patterns

- Component organization: planned Streamlit app under `drivers/ui/streamlit/` with one workbench flow and supporting pages or widgets
- State management rule: UI state stays view-local; authoritative workflow state lives in the shared graph-owned triage path
- Styling rule: optimize for demo clarity over polish and make the three representative case outcomes visually distinct
- Visibility rule: the workbench should surface disposition, confidence band, rationale, reviewability cues, and the privacy-boundary status

### 7.4 Privacy Boundary Patterns

Subsystem name: pre-model PII guardrail

Why it needs its own section: it is both a scenario contract and a hard architectural seam for every external-model path.

Rules:

- `PIIGuardrailAdapter` is mandatory and provider-agnostic
- raw claim context goes in; tokenized safe context and a reversible token map come out
- raw PII must never cross the external model boundary
- preferred topology is an explicit `tokenize_pii` step before any external model-backed generation node (Lean-Clean `D2`; repo-local topology preference)
- graph state, logs, and traces carry safe tokens or bounded identifiers rather than raw claimant demographics or document text after tokenization (Lean-Clean `B8`, `D2`)
- if a transitional phase temporarily keeps raw claim data in pre-generation graph state, treat that as a deferred-hardening exception only and do not expand the scope of that exception
- the reversible token map stays in a bounded secure process
- a local SLM stretch path may improve token detection, but it must not widen the boundary or absorb broader triage reasoning

### 7.5 Fixture Bundle Patterns

- Canonical fixture location: planned `tests/acceptance/fixtures/death_claim/`
- Required representative cases:
  - `case_a_complete/`
  - `case_b_missing_information/`
  - `case_c_ambiguous/`
- Fixture rule: fixtures stay small, hand-authored, deterministic, and readable
- Reuse rule: the same fixtures should drive acceptance tests, smoke paths, and privacy assertions
- Anti-pattern: do not replace the canonical fixtures with a synthetic-data pipeline before the first thin slice is stable

---

## 8. Testing & Verification

### 8.1 Testing Strategy

- Overall strategy: acceptance-first, with targeted unit coverage for pure policy and guardrail logic plus smoke coverage for delivery surfaces
- Test priorities: representative-case routing, privacy boundary integrity, bounded dispositions, and shared graph behavior across UI and API
- Required pre-merge checks:
  - current repo: `make format-md` and `make check`
  - planned app slice: `make test` or equivalent once the test runner lands

### 8.2 Unit / Acceptance / Integration Guidance

- Unit tests: required for pure policies, entity helpers, reviewability logic, no-adjudication checks, graph-state mapping, and the PII guardrail boundary
- Acceptance tests: required for behavior changes that affect representative triage outcomes, artifact generation, or disposition rules
- Integration or smoke tests: required for the graph-owned path and for thin API or UI wiring changes
- End-to-end or manual verification: required for the demo path using live model calls and for any change that could affect privacy handling or reviewer-facing behavior

### 8.3 Fakes Vs Fixtures / Mocks

- Fakes: planned under `app/adapters/*/fake.py` to keep tests deterministic and let the graph stabilize without broad infrastructure
- Fixtures: planned under `tests/acceptance/fixtures/death_claim/` as the canonical representative case bundles
- Mocks or spies: allowed only for narrow edge assertions when a fake would add needless complexity
- Graph tests: keep graph compilation, state mapping, and deterministic routing tests separate from live-model or surface-wiring tests
- Anti-pattern: do not duplicate scenario truth across many one-off mocks or tests that drift away from the three canonical fixture bundles

### 8.4 Required Validation For New Patterns

When introducing a new reusable pattern, also add:

- the tests or manual validation needed at the affected boundary
- an update to `docs/patterns.md` or the narrower doc that now owns the pattern
- a short canonical example or anti-pattern when the pattern is easy to misuse

---

## 9. Examples & Anti-Patterns

### 9.1 Canonical Examples

```python
# planned drivers/api/routes/triage.py
async def post_triage(payload: DeathClaimRequest, deps: ApiDeps):
    request = ApiRequestMapper().to_triage_request(payload)
    graph_state = TriageGraphState.from_request(request)
    result = await deps.death_claim_triage_graph.ainvoke(graph_state)
    return TriageResultPresenter().to_api_response(result)
```

This is correct because the driver stays thin, mapping happens once, the graph owns workflow runtime, and presentation stays at the edge.

```python
# additional canonical example: graph factory with closure-based adapter injection
@dataclass(slots=True, frozen=True)
class AdapterRegistry:
    document_store: DocumentStoreProtocol
    policy_lookup: PolicyLookupProtocol
    review_queue: ReviewQueueProtocol
    pii_guardrail: PIIGuardrailAdapter
    evaluation_recorder: EvaluationRecorderProtocol


def build_triage_graph(adapters: AdapterRegistry) -> CompiledStateGraph:
    workflow = StateGraph(TriageGraphState)

    def assess_triage(state: TriageGraphState) -> dict:
        disposition = DecideTriageDispositionUseCase().execute(
            state["is_complete"], state["is_ambiguous"]
        )
        return {"disposition": disposition}

    workflow.add_node("assess_triage", assess_triage)
    return workflow.compile()
```

This is correct because dependencies are injected through a registry and closures, the graph state stays transport-like, and business logic still lives behind typed use-cases, consistent with Lean-Clean `B8` and `C8`.

```python
# additional canonical example: state accumulation with explicit reducers and final mapping
class TriageGraphState(TypedDict, total=False):
    claim_bundle: ClaimIntakeBundle
    disposition: str
    escalation_reasons: Annotated[list[str], operator.add]


def map_state_to_triage_result(state: TriageGraphState) -> TriageResult:
    return TriageResult(
        disposition=state.get("disposition", "unknown"),
        escalation_reasons=state.get("escalation_reasons", []),
    )
```

This is correct because additive fields use explicit reducers and the graph state is mapped back into the domain result at the edge, consistent with Lean-Clean `A2.1` and `B8`.

```python
# additional canonical example: structured LLM output mapped immediately at the boundary (Lean-Clean Rule B9/C3)
from pydantic import BaseModel, Field

# 1. Pydantic schema lives ONLY in the adapter/gateway
class RequirementsChecklistSchema(BaseModel):
    items: list[str] = Field(description="Missing documents needed")

# 2. LangChain parses against the Pydantic schema
result = llm.with_structured_output(RequirementsChecklistSchema).invoke(prompt)

# 3. Map immediately into the frozen Domain dataclass before returning to use-cases/graph
return CompletenessAssessment(
    is_complete=False,
    missing_items=tuple(result.items)
)
```

This is correct because the vendor-specific Pydantic schema and the LangChain parsing mechanics are fully contained in the adapter, preventing Pydantic from bleeding into the immutable Domain layer (Lean-Clean `Golden Rule 3`).

```python
# additional canonical example: Elysia-style DSPy Signature (Lean-Clean Rule 7.1.5)
import dspy

class AssessReviewability(dspy.Signature):
    """
    You are a triage routing agent. Your goal is to determine if a claim contains enough
    legible information for a human to review it, or if it must be rejected outright.

    Core Analysis Process:
    1. Read the parsed OCR text of the claim documents
    2. Check if the core identifying fields (Name, SSN, Date of Death) are legible
    3. Determine if the document represents a death claim

    Decision Rules:
    - If the document is completely illegible, it is NOT reviewable
    - If it is clear the document is NOT a death claim (e.g. it is a car insurance policy), it is NOT reviewable
    """

    ocr_text: str = dspy.InputField(
        desc="Parsed text from the claimant's uploaded documents. Use this to determine if the text is legible and relevant."
    )

    reasoning: str = dspy.OutputField(
        desc="""
        A 2-3 sentence explanation of your decision.

        Your reasoning should address:
        - Whether the text was legible
        - Whether the document type was correct

        Example: "The uploaded document is a clear, legible scan of a death certificate. Therefore it is reviewable."
        """
    )

    is_reviewable: bool = dspy.OutputField(
        desc="True if a human can review this claim, False if it must be rejected as illegible/irrelevant."
    )
```

This is correct because it treats the Signature as a comprehensive instruction set. It defines the role, goal, and rules in the docstring. It uses `desc=` on every field to explain formatting and constraints, and it requires a `reasoning` field for transparency BEFORE the final boolean decision is made.

```python
# additional canonical example: Layered Guardrails (Lean-Clean Rule D2)
@dataclass(slots=True, frozen=True)
class GuardrailDecision:
    allowed: bool
    reason: str | None = None

def pre_model_guardrail(user_text: str) -> GuardrailDecision:
    if "password" in user_text.lower():
        return GuardrailDecision(False, "Blocked before model call: sensitive input.")
    return GuardrailDecision(True)

def post_model_guardrail(answer: str, citations: tuple[str, ...]) -> GuardrailDecision:
    if not citations:
        return GuardrailDecision(False, "Blocked after model call: no citations.")
    return GuardrailDecision(True)
```

This is correct because guardrails are implemented as explicit, deterministic layers (pre-model, post-model, retrieval, output) rather than a single black-box LLM call or middleware hook.

```python
# additional canonical example: Deterministic Routing (Lean-Clean Rule D3)
from enum import StrEnum

class RouteName(StrEnum):
    direct = "direct"
    retrieve = "retrieve"
    escalate = "escalate"

@dataclass(slots=True, frozen=True)
class RouterDecision:
    route: RouteName
    reason: str

def route_request(user_text: str) -> RouterDecision:
    text = user_text.lower()
    if "approve" in text or "exception" in text:
        return RouterDecision(RouteName.escalate, "Human decision required.")
    if "policy" in text:
        return RouterDecision(RouteName.retrieve, "Explicit knowledge-backed route.")
    return RouterDecision(RouteName.direct, "Simple request.")
```

This is correct because the system defaults to deterministic routing based on bounded `StrEnum` outcomes instead of asking an LLM to hallucinate a path. Routing logic is testable and explicit.

### 9.2 Anti-Patterns

```python
# bad: raw PII crosses the model boundary and business logic is embedded in the graph
async def triage_node(state, openai_client):
    prompt = f"Review claimant {state.claimant_name} and SSN {state.claimant_ssn}"
    response = await openai_client.responses.create(model="gpt-4.1", input=prompt)
    if "missing" in response.output_text.lower():
        state.disposition = "request_more_information"
    else:
        state.disposition = "proceed"
    return state
```

This is incorrect because it sends raw PII to an external model, hides routing policy inside the graph node, mutates untyped state, and bypasses the adapter and use-case boundaries. That violates Lean-Clean `D3`, `B8`, and `C8`, plus the repo-local privacy boundary.

```python
# bad: graph state carries runtime dependencies and prompt ownership
class BadGraphState(TypedDict):
    claim_bundle: ClaimIntakeBundle
    openai_client: Any
    prompt_template: str
```

This is incorrect because graph state is for workflow data, not runtime clients or prompt management. That violates Lean-Clean `B8` and `C8`.

### 9.3 Migration Guidance

As code lands:

1. Replace planned-path language with implemented-path references
2. Move stable rules from planning docs into enforced code and tests
3. Narrow provisional rules only when the defer register is intentionally closed
4. Avoid large-bang rewrites; migrate boundary by boundary while preserving the representative fixture contract

---

## 10. Change Log & Maintenance

### 10.1 Change Log

- `2026-03-10`: Initial repo-specific version created from `.scratch/patterns.template.md` and the current death-claim planning docs
- `2026-03-11`: Added concrete LangGraph, LLM-boundary, and future DSPy implementation patterns based on `plan/implementation/` and the LangGraph decision record

### 10.2 Open Gaps / TODOs

- The exact missing-vs-ambiguous threshold remains provisional and must follow `plan/death-claim/deferred-hardening.md`.
- The claimant-facing tone rubric remains provisional and must follow `plan/death-claim/deferred-hardening.md`.
- The governance and data-science review scorecard remains provisional and must follow `plan/death-claim/deferred-hardening.md`.
- The confidence and reviewability rubric remains provisional and must follow `plan/death-claim/deferred-hardening.md`.
- Planned Tree A file paths should be converted to implemented references as the repo gains code.

### 10.3 Ownership / Review Cadence

- Owner: repo maintainer
- Review cadence: per milestone and whenever architecture materially changes
- Trigger updates when: the bounded result shape changes, a new delivery surface is added, a fake-backed boundary becomes a live integration, or a provisional hardening item is closed
