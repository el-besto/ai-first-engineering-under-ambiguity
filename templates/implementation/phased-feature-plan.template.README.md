# Phased Feature Plan Template: Usage Guide

## Purpose

The `phased-feature-plan.template.md` is designed to break down a large execution block (such as an epic, a workshop scenario, or a Tree A slice) into smaller, reviewable implementation phases.

It provides an explicit contract boundary to ensure that an AI agent or a secondary developer doesn't accidentally expand scope into future phases.

## When to Use

Use this template when:

- An approved `acceptance-contract-plan` or architectural design doc is too large for a single PR or a single uninterrupted agent coding session.
- You need explicit "stop and review" points between discrete chunks of work (e.g., building a database schema before wiring an API, or building deterministic rules before injecting live LLM calls).

Do **NOT** use this template when:

- The work is simple enough to be completed in one sitting (use standard task lists or PR descriptions).
- You are documenting a completed slice to stakeholders (use `slice-change-report.template.md`).

## How to Use

1. **Copy the Template:**
   Create a new file in `plan/implementation/` named `<feature>-phase-<N>-<name>.md`.
   *Example: `plan/implementation/langgraph-phase-1-state.md`*

2. **Define Strict Boundaries:**
   Fill in the `Contract Inputs` and `Out Of Scope` sections carefully. If an agent is executing this phase, it relies heavily on those boundaries to know what *not* to touch.

3. **Leave Lists Open:**
   When listing assertions, files, or execution steps, use the `*(Add as many... as needed)*` syntax to prevent agents from truncating lists prematurely.

4. **Review Cycle:**
   Treat each phase document as a rigid contract. An agent or developer must complete the `Verification Plan` exactly as written before progressing to Phase N+1.
