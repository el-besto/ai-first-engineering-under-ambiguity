<!-- AGENT INSTRUCTION: You MUST read `templates/decision/decision-document-template.README.md` before using this template to create a new decision record. Do not alter the structure of this document. -->
# Observability Standardization: Decisions Needed

> **Template Version:** 1.0 (2025-10-13)
>
> **Usage Instructions:** See `templates/decision/decision-document-template.README.md` for how to use this template and how it fits into the repo's decision-record workflow.
>
> **Related Template:** Use this document when a cross-cutting repo or implementation decision needs explicit options, rationale, and status tracking.

---

**Status:** ✅ 2 of 2 Resolved | 0 Awaiting Discussion

This document captures the cross-cutting observability decisions for aligning `bestow-poc` with the structured logging conventions already used in `career-map`, while preserving the repo's Lean-Clean layering rules.

**Related source-of-truth docs:**

- `docs/patterns.md`
- `app/infrastructure/telemetry/logger.py`

---

## Summary Table

| Decision | Topic                              | Priority | Status     |
|----------|------------------------------------|----------|------------|
| 1        | Logging boundary and context shape | HIGH     | ✅ RESOLVED |
| 2        | Sensitive-data logging posture     | HIGH     | ✅ RESOLVED |

---

## Decision 1: Logging Boundary And Context Shape ⚠️

**Agent Analysis:**

- `bestow-poc` already had a basic `structlog` setup, but it was missing the stronger conventions from `career-map`: component binding, operation binding, short lifecycle events, and consistent failure logging.
- The repo's own `docs/patterns.md` only captured a thin version of the logging rules, so the implementation and source-of-truth were both underspecified.

**Context:**
We needed to decide whether observability should remain lightweight and ad hoc or follow the same structured boundary placement used elsewhere: drivers, thin graph wrappers, and adapters that touch I/O.

**Decision Required:**
Where should structured observability live, and what context shape should be standard?

- [x] **Option A: Drivers, thin graph wrappers, and I/O adapters bind component and operation context**
  - Use bound component fields such as `driver`, `adapter`, `orchestrator`, and `node`, plus per-method `operation`.
  - ✅ Pro: Matches the `career-map` pattern and keeps telemetry out of entities and use-cases.
  - ✅ Pro: Produces uniform `started` / `completed` / `failed` events with stable searchable fields.
  - ❌ Con: Requires touching multiple entrypoints and adapters instead of leaving logging concentrated in one place.

- [ ] **Option B: Keep logging mostly at API/UI entrypoints**
  - Only middleware and route handlers log, with limited step visibility below that boundary.
  - ✅ Pro: Smaller implementation surface.
  - ❌ Con: Leaves graph execution and adapter behavior opaque during debugging and demos.

- [ ] **Option C: Push logging into use-cases and entities for maximum detail**
  - Add logs directly inside core business logic.
  - ✅ Pro: High internal visibility.
  - ❌ Con: Violates the repo's clean boundary posture and couples the core to observability concerns.

**Agent Recommendation:** Option A

**Reasoning:**
This is the only option that preserves the repo's architecture while giving enough run visibility for the API, Streamlit workbench, and LangGraph flow.

**User Decision:** ✅ **Option A: Drivers, thin graph wrappers, and I/O adapters bind component and operation context**

**Rationale:**
The user explicitly called out the missing migration of existing observability patterns and pointed to the `career-map` logging section as the desired source.

**Impact:** HIGH - affects repo-wide logging shape, debugging posture, and source-of-truth documentation.

**Status:** ✅ RESOLVED

---

## Decision 2: Sensitive-Data Logging Posture ⚠️

**Agent Analysis:**

- The existing API route logged the raw `policy_number`, and the project had no explicit implementation-level guardrails for avoiding raw prompt logging beyond a short note in `docs/patterns.md`.
- This PoC handles claim bundles and PII, so observability needs to prefer safe derived fields over raw payloads.

**Context:**
We needed to decide whether logs should ever include raw policy identifiers, prompts, or claim content for convenience, especially in local development.

**Decision Required:**
What is safe to log, and what must stay out of logs entirely?

- [x] **Option A: Log only safe derived fields**
  - Allow counts, lengths, generated field names, adapter modes, disposition metadata, and correlation identifiers like `case_id` or request/session IDs.
  - ✅ Pro: Preserves debugging value without leaking raw claim content, prompts, token maps, or credentials.
  - ✅ Pro: Aligns with the privacy boundary already present in the graph.
  - ❌ Con: Some deep debugging requires replaying the flow locally instead of inspecting raw logs.

- [ ] **Option B: Allow raw prompts and identifiers in development only**
  - Keep production logs clean but relax the rule for local work.
  - ✅ Pro: Easier ad hoc debugging.
  - ❌ Con: Increases accidental leakage risk and makes local behavior diverge from the standard.

- [ ] **Option C: Leave the rule informal**
  - Rely on reviewer judgment case by case.
  - ✅ Pro: No upfront implementation work.
  - ❌ Con: Repeats the current problem where the repo standard is too easy to miss or apply inconsistently.

**Agent Recommendation:** Option A

**Reasoning:**
The PoC already depends on a privacy seam. Logging raw prompts, policy numbers, or claim content would undercut that seam for very limited benefit.

**User Decision:** ✅ **Option A: Log only safe derived fields**

**Rationale:**
The `career-map` guidance the user referenced explicitly treats prompts and sensitive identifiers as out of bounds for logs; the repo now mirrors that rule.

**Impact:** HIGH - affects privacy posture, debugging norms, and route/adapter logging content.

**Status:** ✅ RESOLVED

---

## Next Steps

**Completed:**

- ✅ Updated `docs/patterns.md` to document the stronger logging and tracing conventions.
- ✅ Standardized component and operation binding across API, Streamlit, graph nodes, orchestrators, and active adapters.
- ✅ Replaced ad hoc error logging with `log_exception(...)` at the affected boundaries.
- ✅ Added regression coverage for graph observability output.

**Awaiting Input (0 decisions):**

- None

**After Decisions Resolved:**

1. Keep future driver, graph-wrapper, and adapter work aligned with the updated `docs/patterns.md` conventions.
2. Extend the same pattern to any new live integrations that enter the repo later.

**Status:** 2 of 2 decisions resolved | 0 awaiting collaborative review
