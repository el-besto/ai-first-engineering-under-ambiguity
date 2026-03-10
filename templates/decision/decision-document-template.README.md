# Decision Document Template

**Purpose:** This template is for the **decision artifact** created during collaborative work in this repo. It tracks architectural decisions, presents options, documents choices, and serves as the single source of truth for why a cross-cutting choice was made.

---

## Relationship To Implementation Work

This template is for the decision-discovery phase that happens before implementation or documentation changes are finalized.

Typical flow:

```text
You: describe a task or a repo-wide change
  ↓
Agent: analyzes the task and current repo docs
  ↓
Agent: creates a decision record using this template
  ↓
Agent: presents options and trade-offs
  ↓
You: choose options and provide rationale
  ↓
Agent: updates the decision record with resolved outcomes
  ↓
Agent: updates source-of-truth docs based on the resolved decisions
```

---

## Usage Notes

### When To Create A Decision Record

Create a decision record when a change affects:

1. source-of-truth ownership
2. implementation posture or repo structure
3. naming or terminology with broad repo impact
4. scope boundaries that materially affect multiple docs or systems
5. another cross-cutting choice that should be reviewable later

Do **not** create a decision record for trivial wording-only edits.

### What Goes In The Decision Record

For each decision, include:

- a clear statement of what needs to be decided
- why it matters
- relevant repo or research context
- 2-3 viable options with trade-offs
- the agent's recommendation
- the user's decision
- the rationale for the decision
- impact and status

The document should also include:

- a summary table of all decisions
- a short next-steps section
- links to related source-of-truth docs

### Document Lifecycle

1. **Created** during decision discovery
2. **In progress** while decisions are still open
3. **Resolved** as choices are made
4. **Implemented** when the affected source-of-truth docs are updated
5. **Retained** in `plan/decisions/` as the permanent rationale record

### File Naming Convention

Use descriptive names that match the topic:

- `_repo-planning-decisions.md`
- `_framework-structure-decisions.md`
- `_terminology-decisions.md`

The underscore prefix indicates a working or planning artifact rather than a final product deliverable.

---

## Repo-Specific Notes

- Reusable blank decision templates belong in `templates/decision/`.
- Live filled-in decision records belong in `plan/decisions/`.
- When a decision is resolved, update the affected source-of-truth docs in the same change.
- If scratch content is promoted into a VCS-tracked doc, keep the original scratch headers and replace the extracted body with a link to the new destination.

---

## Template Structure

The template provides:

### Header Section

- task name and overall status
- quick summary of resolved vs awaiting decisions
- update notes as new decisions are discovered

### Decision Entries

Each decision includes:

- title with optional priority marker
- "What I did"
- "Context"
- "Question for you"
- options with pros and cons
- recommendation and reasoning
- decision and rationale
- impact
- status

### Summary Table

Use the summary table to show:

- decision number and name
- priority
- status

### Next Steps

Use the next-steps section to capture:

- what has already been completed
- what remains open
- what should happen after the decisions are resolved

---

## Maintenance

**Location:**

- bare template: `templates/decision/decision-document-template.md`
- usage notes: `templates/decision/decision-document-template.README.md`

**Version:** 1.0 (2025-10-13)

Update this template when:

- the repo develops a better decision-record pattern
- additional metadata proves useful
- planning workflow changes materially
