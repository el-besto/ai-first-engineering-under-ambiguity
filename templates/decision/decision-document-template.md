<!-- AGENT INSTRUCTION: You MUST read `templates/decision/decision-document-template.README.md` before using this template to create a new decision record. Do not alter the structure of this document. -->
# [Task Name]: Decisions Needed

> **Template Version:** 1.0 (2025-10-13)
>
> **Usage Instructions:** See `templates/decision/decision-document-template.README.md` for how to use this template and how it fits into the repo's decision-record workflow.
>
> **Related Template:** Use this document when a cross-cutting repo or implementation decision needs explicit options, rationale, and status tracking.

---

**Status:** 🚧 0 of 0 Resolved | 0 Awaiting Discussion

This document captures the key decisions for [brief description of task].

**Update:** [Add notes here as new decisions are discovered during analysis]

---

## Decision 1: [Decision Name] ⚠️ [Add CRITICAL flag if applicable]

**Agent Analysis:**

- [Describe the analysis already completed]
- [If nothing has started yet, note that the decision was identified during analysis]

**Context:**
[Relevant background from repo docs, analysis, or prior decisions]

**Decision Required:**
[Clear framing of what needs to be decided]

- [ ] **Option A: [Name]** ([brief descriptor])
  - [Brief description of the approach]
  - ✅ Pro: [Benefit]
  - ✅ Pro: [Benefit]
  - ❌ Con: [Drawback]
  - ❌ Con: [Drawback]

- [ ] **Option B: [Name]** ([brief descriptor])
  - [Brief description of the approach]
  - ✅ Pro: [Benefit]
  - ✅ Pro: [Benefit]
  - ❌ Con: [Drawback]
  - ❌ Con: [Drawback]

- [ ] **Option C: [Name]** ([brief descriptor])
  - [Brief description of the approach]
  - ✅ Pro: [Benefit]
  - ❌ Con: [Drawback]

**Agent Recommendation:** Option [A/B/C/X...]

**Reasoning:**
[Why this option best fits the requirements and repo context]

**User Decision:** [AWAITING INPUT] or ✅ **Option X: [Name]**

**Rationale:**
[Space to capture the decision rationale]

**Impact:** [CRITICAL/HIGH/MEDIUM/LOW] - [Brief description of what this affects]

**Status:** 🚧 AWAITING or ✅ RESOLVED

---

## Decision N: [Decision Name]

Copy the structure from Decision 1 for additional decisions.

---

## Summary Of Decisions

| # | Decision             | Priority                   | Status                     |
|---|----------------------|----------------------------|----------------------------|
| 1 | [Decision Name]      | [CRITICAL/HIGH/MEDIUM/LOW] | [🚧 AWAITING / ✅ RESOLVED] |
| 2 | [Decision Name]      | [Priority]                 | [Status]                   |
| N | [Add rows as needed] | [Priority]                 | [Status]                   |

**Priority Levels:**

- ⚠️ **CRITICAL**: fundamental architecture or source-of-truth decision
- **HIGH**: significant implementation or coordination impact
- **MEDIUM**: important but localized impact
- **LOW**: minor impact and easy to change later

---

## Next Steps

**Completed:**

- ✅ [List completed analysis or preparation]
- ✅ [Reviewed relevant documentation]

**Awaiting Input ([X] decisions):**

1. **Decision X: [Name]**
2. **Decision Y: [Name]**

**After Decisions Resolved:**

1. [Update affected source-of-truth docs]
2. [Adjust implementation or planning artifacts]
3. [Record any follow-on work]

**Status:** [X] of [Y] decisions resolved | [Z] awaiting collaborative review

---

## Notes

**Decision Discovery Process:**

- [Document how these decisions were identified]
- [Track dependencies between decisions if needed]

**Related Documents:**

- [Link to related repo docs]
- [Link to prior decision records if relevant]
