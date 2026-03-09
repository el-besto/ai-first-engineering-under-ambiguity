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
- Before a commit that delivers completed work, ensure related checklist items in [PLAN.md](PLAN.md) are updated in the same commit when appropriate.

### 1.2 Markdown and Documentation Workflow

- Run `make format-md` before `git commit` if Markdown files were changed.
- Use repo-relative paths in repo-authored Markdown.
- Keep `AGENT_RULES.md` as the single source of truth for agent instructions. [AGENTS.md](AGENTS.md) and [GEMINI.md](GEMINI.md) should remain thin pointers.

### 1.3 Safe File Modification

- Avoid blind deletions or broad replacements without verifying the exact target content.
- Immediately review the resulting diff after file modifications to confirm that no unintended content was changed.
