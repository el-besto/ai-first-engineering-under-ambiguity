# Patterns & Conventions - bestow-poc

**Purpose:** Repo-wide v1 implementation policy for `bestow-poc`, grounded in the
current death-claim steel thread and Lean-Clean Tree A baseline.

**Maintenance Note:** This repo is still doc-first. When this document names
paths under `app/`, `drivers/`, `deploy/`, or `tests/`, treat them as planned
Tree A locations from `plan/death-claim/tree-a-code-map.md` unless the paths
already exist in the repo.

**Related-Doc Precedence:** Follow the precedence rules in Section 1.4. For
provisional hardening items, defer to
`plan/death-claim/deferred-hardening.md` until those items are intentionally
hardened.

---

## 1. Document Purpose & Usage

### 1.1 Purpose

`bestow-poc` uses this document to define the implementation patterns that all
planned app code, tests, scripts, docs, and committed demo artifacts must
follow.

### 1.2 Scope

This document applies to:

- planned production app code for the death-claim PoC
- tests and acceptance fixtures
- repo automation and support scripts
- repo-authored documentation and demo artifacts that describe or constrain the
  implementation

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
   - `plan/death-claim/workshop-spec.md`
   - `plan/death-claim/steel-thread.md`
   - `plan/implementation/repo-bootstrap-plan.md`
   - `plan/implementation/tooling-validation-plan.md`
   - `plan/implementation/acceptance-contract-plan.md`
   - `plan/death-claim/tree-a-code-map.md`
   - `plan/death-claim/tree-a-worked-example.md`
3. `docs/patterns.md`
4. Historical or execution-draft artifacts under `.scratch/`

Repo-specific exception:

- For rules marked provisional in this document, the active defer register is
  `plan/death-claim/deferred-hardening.md`.

---

## 2. Agent Playbook

### 2.1 Objective

Keep `docs/patterns.md` accurate, minimal, and directly actionable for
implementers and reviewers while the repo moves from planning to code.

### 2.2 Inputs To Inspect

Inspect these sources before updating this document:

- `AGENT_RULES.md`
- `PROJECT_PLAN.md`
- `Makefile`
- `.pre-commit-config.yaml`
- `.markdownlint-cli2.yaml`
- `.editorconfig`
- `cspell.config.yaml`
- `plan/implementation/repo-bootstrap-plan.md`
- `plan/implementation/tooling-validation-plan.md`
- `plan/implementation/acceptance-contract-plan.md`
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
- a rule would move business logic out of use-cases or entities and into a
  graph, UI, or driver
- a change would relax the PII boundary or no-adjudication guardrails
- two repo docs conflict and current code does not resolve the conflict
- a provisional hardening item is about to become acceptance-driving behavior

### 2.5 Verification Checklist

Before finalizing an update, verify:

- every rule is grounded in repo code, enforced config, or the higher-precedence
  docs listed above
- planned Tree A paths are labeled as planned when the files do not yet exist
- provisional items still point back to
  `plan/death-claim/deferred-hardening.md`
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

- [ ] Tree A layering is preserved and graph nodes stay thin wrappers around
      use-cases, ports, or adapter calls
- [ ] Use-cases depend only on domain types and adapter `protocol.py`
      contracts, never on concrete `fake.py`, provider implementations, or
      driver/framework types
- [ ] Tests cover the affected boundary: acceptance fixtures for triage
      behavior, unit checks for guardrails and pure policies, and smoke coverage
      for graph/API/UI paths as needed
- [ ] Raw PII never crosses the external model boundary, the PoC never implies
      adjudication or benefit determination, and human-review boundaries remain
      explicit
- [ ] Streamlit and FastAPI call the same graph-owned triage path and return one
      bounded disposition per run

### 3.2 Architectural Invariants

- Dependencies flow inward through the Tree A layers:
  `drivers -> interface_adapters -> use_cases -> adapter contracts/domain`.
- Domain logic must not depend on FastAPI, Streamlit, LangGraph runtime types,
  vendor SDKs, storage clients, prompt templates, or raw transport schemas.
- Cross-layer transformations happen in mappers, presenters, parsers, and
  adapter boundaries, not in entities or use-cases.
- LangGraph owns workflow runtime, but business rules stay in entities and
  use-cases.
- Graph state must not carry raw PII, vendor clients, prompt templates, or
  persistence handles.
- Every triage run ends in exactly one bounded disposition:
  `proceed`, `request_more_information`, or
  `escalate_to_human_review`.

### 3.3 Allowed Exceptions

- Driver dependency modules may construct concrete adapters, choose fake versus
  live implementations, and manage client lifecycle.
- Driver-edge request or response schemas may use framework-specific models, but
  they must be mapped inward immediately.
- Small adapter-local parsing schemas for structured LLM output are allowed if
  they remain outside the application core and are mapped immediately into
  internal types.
- Fake adapters are allowed for deterministic tests, local demo scaffolding,
  and early graph stabilization.

### 3.4 Definition Of Done

A change is not complete until:

- it follows the rules in this document or records an intentional exception in a
  higher-precedence doc
- required tests or manual validations for the affected boundary are present or
  explicitly waived
- any new reusable repo-wide pattern is documented here or in a narrower
  source-of-truth doc
- reviewers can trace the change to the correct Tree A layer

---

## 4. Core Architecture Patterns

### 4.1 Domain Model Patterns

- Primary domain model type: immutable Python dataclasses in planned
  `app/entities/`
- Mutability rule: immutable by default with `@dataclass(slots=True, frozen=True)`
- Validation rule: transport and payload shape validation happens at the driver
  edge; business invariants live in entity constructors/helpers and use-case
  policy
- Boundary rule: domain models must not import framework code, vendor SDKs,
  storage clients, prompt templates, or tracing libraries

Canonical planned v1 domain and result types:

- `ClaimIntakeBundle`
- `CompletenessAssessment`
- `AmbiguityAssessment`
- `ReviewabilityAssessment`
- `TriageDisposition`
- `TriageResult`

### 4.2 Use Case / Service Patterns

- Primary unit of orchestration: use-case modules or classes in planned
  `app/use_cases/`
- Input shape: typed request models or command-style dataclasses assembled once
  by a mapper, controller, or graph wrapper
- Output shape: typed domain results and artifact models, with `TriageResult` as
  the bounded end-state contract for the v1 flow
- Side-effect policy: all I/O is isolated behind adapter contracts in planned
  `app/adapters/*/protocol.py`

Rules for use-cases:

- Keep routing, completeness, ambiguity, reviewability, and no-adjudication
  policy out of the graph runtime
- Depend on adapter protocols only, never on concrete `fake.py` or provider
  implementations
- Return typed results that make ambiguity and escalation explicit instead of
  hiding those outcomes in exceptions

### 4.3 Repository Patterns

The v1 slice is fake-backed and in-memory by default, so the primary boundary is
the adapter contract rather than a broad persistence layer.

- Interface location: planned `app/adapters/policy_lookup/protocol.py`,
  `app/adapters/document_intake/protocol.py`,
  `app/adapters/model/protocol.py`,
  `app/adapters/safety/protocol.py`, and
  `app/adapters/review_queue/protocol.py`
- Implementation location: planned `app/adapters/*/fake.py` for deterministic
  collaborators, plus planned provider or parser modules where live integrations
  are required
- Return type guidance: use concrete domain dataclasses for single operations
  and `Sequence[...]` for ordered collections; do not leak raw vendor payloads
  or ad hoc dict shapes across the boundary
- Conversion boundary: persistence, storage, or vendor payloads become typed
  domain entities or typed facts inside adapters and parsers before reaching
  use-cases or graph state

Broad `app/infrastructure/` concerns remain deferred unless the slice expands
beyond the current steel thread.

### 4.4 Mapper Vs Presenter Patterns

- Mapper purpose: convert workbench and API input into internal request models
  and initial graph state once
- Presenter purpose: convert typed internal results into outbound UI or API
  views once and attach edge observability
- Anti-confusion rule: mappers do not format outbound views, and presenters do
  not decide dispositions or repair incomplete domain data

Planned Tree A mapper and presenter locations:

- `app/interface_adapters/mappers/workbench_request_mapper.py`
- `app/interface_adapters/mappers/api_request_mapper.py`
- `app/interface_adapters/mappers/response_mapper.py`
- `app/interface_adapters/presenters/triage_result_presenter.py`
- `app/interface_adapters/orchestrators/triage_graph_state.py`

### 4.5 Dependency Injection / Composition Root

- Composition root location: planned `drivers/api/dependencies.py` and planned
  `drivers/ui/streamlit/dependencies.py`
- Injection style: manual wiring from driver dependency modules into the graph,
  orchestrator, use-cases, and adapters
- Ownership rule: drivers and dependency modules create and close external
  clients; entities, use-cases, and graph state do not own client lifecycle

Primary planned delivery entrypoints:

- Streamlit workbench under `drivers/ui/streamlit/`
- FastAPI `GET /health`
- FastAPI `POST /triage`

### 4.6 Configuration Management

- Primary config mechanism: small settings or dependency-wiring objects loaded
  from environment variables and local `.env` support at the driver/config layer
- Allowed direct env access: config and dependency wiring only, plus short-lived
  repo automation scripts
- Required defaults and override policy: default to fake-backed local operation,
  local-first tracing, and opt-in live provider credentials for the demo path

---

## 5. Cross-Cutting Conventions

### 5.1 Naming And Code Style

- Primary language: Python for the planned app slice, Markdown for repo docs and
  planning artifacts
- Naming conventions: snake_case for modules and functions, PascalCase for
  classes, `Literal` or `StrEnum` for bounded dispositions and confidence bands
- Formatting and linting tools:
  - current repo: `make format-md`, `tools/format-markdown.cjs`,
    `.markdownlint-cli2.yaml`, `pre-commit`, `cspell`
  - planned app baseline: `uv`, Ruff, and Pyright, consistent with
    `PROJECT_PLAN.md` and `plan/implementation/repo-bootstrap-plan.md`
- Type annotation policy: full annotations are required for app code, protocols,
  graph state, boundary DTOs, and tests that cross architectural boundaries

### 5.2 Logging

- Log using the app-configured logger from drivers, presenters, and adapters
  that touch I/O
- Event naming rule: use short operation-oriented events tied to the triage step
  or delivery surface
- Required context: case or bundle identifier, surface, selected disposition,
  confidence band, and reviewability state
- Forbidden patterns: `print` in planned app code, raw prompt logging, raw PII
  logging, and silent guardrail failures

### 5.3 Error Handling

- Surface errors at the driver boundary
- Wrap or normalize errors using typed application or adapter errors before they
  reach UI or HTTP responses
- Re-raise vs absorb rule: inner layers re-raise typed errors; drivers and
  presenters translate them into bounded API, UI, or demo-safe failure modes
- Required logging or tracing on failure: record the failing step, adapter, and
  correlation context without raw PII, full claim documents, or raw prompts

Business ambiguity is not an exception path. It must be represented by typed
triage results, reviewability flags, or escalation reasons.

### 5.4 Observability / Tracing

- Tracing approach: local-first graph inspection and replay, with initial
  posture `LANGSMITH_TRACING=false`
- Metrics approach: lightweight run visibility is sufficient for v1; a full
  metrics stack is deferred
- Instrumentation boundary: presenters, drivers, and thin graph wrappers add
  traces or run metadata; entities and use-cases remain free of tracing imports
- Do-not-log or do-not-trace rule: raw PII, full raw claim documents, reversible
  token maps, raw prompts, secrets, and provider credentials

---

## 6. Infrastructure & Integration Patterns

### 6.1 Client Lifecycle

- Client config type: config or settings objects passed from dependency modules
- Lifecycle policy: startup or shutdown hooks for API clients, session-scoped
  helpers for Streamlit as needed, and simple process-local fakes for tests or
  local demos
- Ownership rule: drivers and dependency modules close live clients

### 6.2 Persistence Conventions

- Persistence technology: none in v1 beyond in-memory fakes, local acceptance
  fixtures, and transient graph runtime state
- Persistence model rule: if storage is added later, persistence models stay in
  adapters or infrastructure and map inward immediately
- Query or session rule: not applicable in v1; do not add ad hoc storage access
  from use-cases or graph nodes
- Migration rule: deferred until the repo adopts a real store

### 6.3 Vendor Isolation

- Vendor SDKs are allowed in adapters and future infrastructure only
- Vendor response normalization occurs in gateway, parser, or adapter modules
  before data reaches entities, use-cases, presenters, or graph state
- Domain and application layers must not depend on FastAPI, Streamlit,
  LangGraph runtime types, OpenAI or other model SDKs, database clients, or raw
  vendor payload dicts

---

## 7. Optional Extensions

### 7.1 AI / LLM Patterns

- Prompt or signature location: planned `app/adapters/model/prompts/`, with
  parsers in planned `app/adapters/model/parsers/` and live providers in planned
  `app/adapters/model/providers/`
- Structured output rule: use explicit parsers or small adapter-local schemas
  and map immediately into internal artifact types
- Model organization rule: deterministic routing, completeness, ambiguity,
  reviewability, and no-adjudication policy stay outside the model; external LLM
  calls are for bounded artifact generation only
- Evaluation and observability rule: keep a fake model adapter for deterministic
  tests, but validate the demo path with live provider-backed runs across the
  representative cases or dispositions
- Stretch-path rule: DSPy or local SLM work is confined to the privacy seam and
  must remain swappable behind `PIIGuardrailAdapter`

### 7.2 API-Specific Patterns

- Request validation location: planned `drivers/api/schemas/` and planned
  `app/interface_adapters/mappers/api_request_mapper.py`
- Response and presenter rule: `POST /triage` validates the request once, maps
  inward once, invokes the shared graph-owned triage path, and returns a
  presenter-shaped bounded response; `GET /health` stays thin and non-domain
- Error envelope rule: driver code translates typed app errors into HTTP
  responses; streaming-specific rules are deferred until streaming exists
- Versioning or compatibility rule: internal v1 API only; keep the contract
  small and aligned with the workbench path

### 7.3 UI / Streamlit Patterns

- Component organization: planned Streamlit app under `drivers/ui/streamlit/`
  with one workbench flow and supporting pages or widgets
- State management rule: UI state stays view-local; authoritative workflow state
  lives in the shared graph-owned triage path
- Styling rule: optimize for demo clarity over polish and make the three
  representative case outcomes visually distinct
- Visibility rule: the workbench should surface disposition, confidence band,
  rationale, reviewability cues, and the privacy-boundary status

### 7.4 Privacy Boundary Patterns

Subsystem name: pre-model PII guardrail

Why it needs its own section: it is both a scenario contract and a hard
architectural seam for every external-model path.

Rules:

- `PIIGuardrailAdapter` is mandatory and provider-agnostic
- raw claim context goes in; tokenized safe context and a reversible token map
  come out
- raw PII must never cross the external model boundary
- graph state, logs, and traces carry safe tokens or bounded identifiers rather
  than raw claimant demographics or document text
- the reversible token map stays in a bounded secure process
- a local SLM stretch path may improve token detection, but it must not widen
  the boundary or absorb broader triage reasoning

### 7.5 Fixture Bundle Patterns

- Canonical fixture location: planned `tests/acceptance/fixtures/death_claim/`
- Required representative cases:
  - `case_a_complete/`
  - `case_b_missing_information/`
  - `case_c_ambiguous/`
- Fixture rule: fixtures stay small, hand-authored, deterministic, and readable
- Reuse rule: the same fixtures should drive acceptance tests, smoke paths, and
  privacy assertions
- Anti-pattern: do not replace the canonical fixtures with a synthetic-data
  pipeline before the first thin slice is stable

---

## 8. Testing & Verification

### 8.1 Testing Strategy

- Overall strategy: acceptance-first, with targeted unit coverage for pure
  policy and guardrail logic plus smoke coverage for delivery surfaces
- Test priorities: representative-case routing, privacy boundary integrity,
  bounded dispositions, and shared graph behavior across UI and API
- Required pre-merge checks:
  - current repo: `make format-md` and `make check`
  - planned app slice: `make test` or equivalent once the test runner lands

### 8.2 Unit / Acceptance / Integration Guidance

- Unit tests: required for pure policies, entity helpers, reviewability logic,
  no-adjudication checks, and the PII guardrail boundary
- Acceptance tests: required for behavior changes that affect representative
  triage outcomes, artifact generation, or disposition rules
- Integration or smoke tests: required for the graph-owned path and for thin API
  or UI wiring changes
- End-to-end or manual verification: required for the demo path using live model
  calls and for any change that could affect privacy handling or reviewer-facing
  behavior

### 8.3 Fakes Vs Fixtures / Mocks

- Fakes: planned under `app/adapters/*/fake.py` to keep tests deterministic and
  let the graph stabilize without broad infrastructure
- Fixtures: planned under `tests/acceptance/fixtures/death_claim/` as the
  canonical representative case bundles
- Mocks or spies: allowed only for narrow edge assertions when a fake would add
  needless complexity
- Anti-pattern: do not duplicate scenario truth across many one-off mocks or
  tests that drift away from the three canonical fixture bundles

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

This is correct because the driver stays thin, mapping happens once, the graph
owns workflow runtime, and presentation stays at the edge.

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

This is incorrect because it sends raw PII to an external model, hides routing
policy inside the graph node, mutates untyped state, and bypasses the adapter
and use-case boundaries.

### 9.3 Migration Guidance

As code lands:

1. Replace planned-path language with implemented-path references
2. Move stable rules from planning docs into enforced code and tests
3. Narrow provisional rules only when the defer register is intentionally closed
4. Avoid large-bang rewrites; migrate boundary by boundary while preserving the
   representative fixture contract

---

## 10. Change Log & Maintenance

### 10.1 Change Log

- `2026-03-10`: Initial repo-specific version created from
  `.scratch/patterns.template.md` and the current death-claim planning docs

### 10.2 Open Gaps / TODOs

- The exact missing-vs-ambiguous threshold remains provisional and must follow
  `plan/death-claim/deferred-hardening.md`.
- The claimant-facing tone rubric remains provisional and must follow
  `plan/death-claim/deferred-hardening.md`.
- The governance and data-science review scorecard remains provisional and must
  follow `plan/death-claim/deferred-hardening.md`.
- The confidence and reviewability rubric remains provisional and must follow
  `plan/death-claim/deferred-hardening.md`.
- Planned Tree A file paths should be converted to implemented references as the
  repo gains code.

### 10.3 Ownership / Review Cadence

- Owner: repo maintainer
- Review cadence: per milestone and whenever architecture materially changes
- Trigger updates when: the bounded result shape changes, a new delivery surface
  is added, a fake-backed boundary becomes a live integration, or a provisional
  hardening item is closed
