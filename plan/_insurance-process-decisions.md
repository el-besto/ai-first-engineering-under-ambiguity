# Insurance Process Selection: Decisions Needed

> **Template Version:** 1.0 (2025-10-13)
>
> **Adapted From:** Lean-Clean decision document template for a process-selection workflow rather than a low-level architecture choice.

---

**Status:** 🚧 0 of 2 Resolved | 2 Awaiting Discussion

This document captures the key decisions for selecting the insurance process to use in the Bestow AI PoC.

**Related Documents:**

- `/docs/references/insurance-processes.md`
- `/PLAN.md`

**Update:** Initial candidate research completed and narrowed to three serious finalists. A pre-existing underwriting workbench demo now introduces novelty risk for underwriting-centered options, so differentiation is an explicit selection criterion.

---

## Decision 1: Which insurance process should this PoC focus on? ⚠️

**What I did:**

- Reviewed life-insurance process candidates
- Compared them for agentic AI fit, Bestow relevance, demoability, and complexity
- Narrowed the field to three strong finalists

**Context:**
The PoC needs to be simple, clearly useful, and suitable for agentic AI. The role is Staff Software Engineer focused on AI deliverables, so the chosen process should support a strong 5-minute demo, a defensible scope, and a credible explanation of how AI assists humans in a regulated workflow. A pre-existing underwriting workbench demo introduces novelty risk for underwriting-centered options, so overlap with familiar underwriting-workbench patterns is now a material evaluation factor. The selected process should still support strong AI orchestration, but should avoid resembling a broad underwriting workbench or document-analysis clone.

**Question for you:**
Which process should anchor the PoC?

- [ ] **Option A: Death claim intake + next-step orchestration** (internal claims intake/triage console)
  - Avoids underwriting-demo overlap while staying strongly life-insurance-specific
  - Clean LangGraph workflow for intake assessment, missing-item detection, routing, and escalation
  - Clear multi-stakeholder story without requiring a two-sided app
  - Still supports generated claimant or beneficiary follow-up as an output artifact
  - Some artifacts still need hand-authored fixtures
  - Tone and copy for claimant-facing drafts need more care than underwriting follow-up
  - Must keep the UI internal-first to stay inside the 3-day scope

- [ ] **Option B: Underwriting case triage / underwriter copilot** (Bestow-aligned AI operations workflow)
  - Strong Bestow relevance and obvious AI value
  - Good fit for summarization, evidence review, and next-step recommendations
  - Strong staff-level technical story around retrieval, summarization, and review tooling
  - Resembles an already-familiar underwriting-workbench category
  - May invite comparison to broader underwriting demos even if scoped differently
  - Creates unnecessary narrative burden in the final presentation
  - Overlap risk is about perceived derivative positioning, not technical infeasibility

- [ ] **Option C: Policy servicing request intake and routing** (cleanest steel-thread workflow)
  - Easiest to prototype and demo in a short time
  - Natural agentic flow: intent classification, guided intake, and routing
  - Strong alignment with administration and customer-portal style workflows
  - Less distinctive as a life-insurance-only process
  - May feel more operationally generic than claims or underwriting

**My recommendation:** Option A: Death claim intake + next-step orchestration

**Reasoning:**
Candidate 1 now provides the strongest combination of differentiation and PoC fit. It best balances life-insurance specificity, stakeholder richness, workflow-first agent design, manageable UX scope, and lower overlap risk with known underwriting demos. It allows the project to showcase agentic orchestration and human-in-the-loop boundaries without entering the same conceptual space as an underwriting workbench demo.

**Your decision:** [AWAITING INPUT]

**Rationale:**
[To fill in once chosen]

**Impact:** HIGH - This determines the user journey, architecture shape, demo narrative, and research depth for the rest of the PoC.

**Status:** 🚧 AWAITING

**Scoping note:**
- Target an internal claims ops workbench, not a claimant-facing app
- Show 3 representative case tabs
- Generated outputs should include a missing-items checklist, claimant or beneficiary follow-up draft, and HITL review task with rationale

---

## Decision 2: How narrowly should the PoC scope the chosen process?

**What I did:**

- Considered the likely time budget, 5-minute demo constraint, and Lean-Clean steel-thread goal
- Narrowed the scoping choices to three realistic slice sizes

**Context:**
Even after choosing the process, the biggest delivery risk is over-scoping the PoC. The take-home likely rewards a clean, credible steel thread more than a broader but shallower implementation. For the claims-oriented direction, the scope should focus on intake assessment, completeness triage, and escalation rather than a full claimant-facing portal.

**Question for you:**
What should the initial PoC boundary be?

- [ ] **Option A: Intake only** (minimal claim intake capture flow)
  - Lowest complexity and fastest path to a working prototype
  - Very easy to demo and explain
  - May feel too thin for a staff-level AI deliverable
  - Leaves less room to show orchestration or downstream system design

- [ ] **Option B: Intake + completeness triage** (recommended steel thread)
  - Best balance of simplicity and substantive AI behavior
  - Shows intake capture, completeness assessment, routing, and next-step logic
  - Supports a stronger end-to-end story without too much implementation weight
  - Allows outputs such as missing-items checklist, claimant follow-up draft, and HITL escalation
  - Slightly more complex than a pure intake flow

- [ ] **Option C: Intake + triage + orchestration preview** (broader systems story)
  - Strongest architecture and systems-thinking demo
  - Creates space to show queues, follow-up tasks, and human review checkpoints
  - Risks over-scoping the implementation for the available time
  - Could spread effort across too many shallow components

**My recommendation:** Option B: Intake + completeness triage

**Reasoning:**
This is the cleanest steel thread. It demonstrates that the AI can do more than collect intake data by producing a completeness assessment, missing-items checklist, claimant or beneficiary follow-up draft, and HITL escalation when ambiguity or mismatch exists, while still stopping short of a broad workflow engine.

**Your decision:** [AWAITING INPUT]

**Rationale:**
[To fill in once chosen]

**Impact:** HIGH - This sets the feature boundary, architecture depth, and demo complexity.

**Status:** 🚧 AWAITING

---

## Summary of Decisions

| #   | Decision                                              | Priority | Status       |
| --- | ----------------------------------------------------- | -------- | ------------ |
| 1   | Which insurance process should this PoC focus on?     | HIGH     | 🚧 AWAITING |
| 2   | How narrowly should the PoC scope the chosen process? | HIGH     | 🚧 AWAITING |

---

## Next Steps

**Completed:**

- ✅ Candidate process research
- ✅ Comparison across decision criteria
- ✅ Shortlist creation

**Awaiting Your Input (2 decisions):**

1. **Decision 1: Which insurance process should this PoC focus on?** ⚠️
2. **Decision 2: How narrowly should the PoC scope the chosen process?**

**After Decisions Resolved:**

1. Update `PLAN.md` checklist if needed
2. Define the target user, success criteria, and steel-thread acceptance criteria
3. Shape the prototype architecture around the selected process and scope
4. Prepare a concise rationale that can be reused in the demo narrative

**Status:** 0 of 2 decisions resolved | 2 awaiting collaborative review

---

## Notes

**Decision Discovery Process:**

- The initial scan emphasized workflows that are simple enough for a short PoC but rich enough to benefit from agentic AI
- The strongest candidates were those where AI can assist intake, summarization, routing, or next-step coordination without replacing regulated human judgment
- Candidate research was intentionally broader than the decision set so the final choice can be defended clearly

**Related Documents:**

- `/docs/references/insurance-processes.md`
- `/PLAN.md`
