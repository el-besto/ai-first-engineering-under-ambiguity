# AGENT_RULES

This file is the single source of truth for repository-specific agent instructions.

## 1. Critical Directives

### 1.1 Git Commit and Push Policy

- Never run `git commit` or `git push` without explicit user permission.
- Never use `git commit --no-verify`.
- If commit hooks modify files, re-check `git status`, re-stage the intended files, and rerun the commit.
- Commit message bodies must use real newlines, not literal `\n` escape sequences.
- When a commit body has multiple points, format it as a short bullet list.
- Prefer separate `-m` arguments or a commit message file for multiline commit messages instead of escaped newline text.
- After writing or amending a multiline commit message, verify the stored format with `git log -1 --pretty=full`.
- Before a commit that delivers completed work, ensure related checklist items in [PROJECT_PLAN.md](PROJECT_PLAN.md) are updated in the same commit when appropriate.

### 1.2 Markdown and Documentation Workflow

- Run `make format-md` before `git commit` if Markdown files were changed.
- Use repo-relative paths in repo-authored Markdown.
- Keep `AGENT_RULES.md` as the single source of truth for agent instructions. [AGENTS.md](AGENTS.md) and [GEMINI.md](GEMINI.md) should remain thin pointers.
- The root repo tracker is [PROJECT_PLAN.md](PROJECT_PLAN.md).
- Planning-document ownership is:
  - [PROJECT_PLAN.md](PROJECT_PLAN.md) for repo-level assignment framing, deliverables, and progress
  - `plan/death-claim/` for the scenario contract and design inputs
  - `plan/implementation/` for live implementation-control docs
  - `plan/decisions/` for cross-cutting decisions and their rationale
  - `templates/` for reusable blanks
  - `.scratch/` for local working notes only, not source of truth
- Create or update a decision document under `plan/decisions/` when a change affects source-of-truth ownership, implementation posture, scope boundaries, naming, or another cross-cutting repo decision. Do not create one for trivial wording-only edits.
- When a decision is resolved, update every affected source-of-truth doc in the same change instead of leaving the resolution isolated in the decision record.

### 1.3 Safe File Modification

- Avoid blind deletions or broad replacements without verifying the exact target content.
- Immediately review the resulting diff after file modifications to confirm that no unintended content was changed.

### 1.4 Implementation Guidance

- Default to established repo patterns and implementation shapes before introducing new structure.
- Consult [docs/patterns.md](docs/patterns.md) when implementation-shape decisions are involved and a canonical pattern exists.
- When similar code, helpers, or modules already exist, prefer reuse, extension, or composition over rewriting from scratch.
- Keep the repo DRY: avoid near-duplicate helpers, parallel code paths, or one-off abstractions that bypass existing logic.
- If you diverge from an established pattern or choose not to reuse an existing function, make the reason explicit in the change or explanation.
