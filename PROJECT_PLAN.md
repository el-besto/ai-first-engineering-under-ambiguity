# Project Plan

## My understanding of the assignment

Bestow wants a short rapid-prototyping exercise that shows how I think as a Staff Software Engineer, not just what I can build.

## Selected direction

- Process: Death claim intake + next-step orchestration
- Scope: Intake + completeness triage
- Primary user: Internal claims operations specialist
- Interaction model: Internal workbench as the primary demo surface, with generated claimant or beneficiary follow-up outputs and a thin internal API over the same graph-owned flow
- Process understanding artifact: [plan/death-claim/process-understanding.md](plan/death-claim/process-understanding.md)
- Detailed planning artifact: [plan/death-claim/steel-thread.md](plan/death-claim/steel-thread.md)

## Progress checklist

- [x] Choose the insurance process or system to focus on
- [x] Research the [current-state process, users, pain points, and constraints](plan/death-claim/process-understanding.md)
- [x] Identify a meaningful improvement opportunity
- [x] Define target user, requirements, assumptions, and success criteria in [plan/death-claim/steel-thread.md](plan/death-claim/steel-thread.md)
- [x] Define the [synthetic data strategy and fixture sources](plan/death-claim/synthetic-data-plan.md) for the chosen workflow
- [x] Establish the minimal Lean-Clean steel-thread structure for the PoC, using `uv`, FastAPI, Ruff, Pyright, Docker, Tilt, and VS Code configuration where they support the chosen slice
- [ ] Build a thin-slice prototype that demonstrates the improvement
- [ ] Prepare demo notes covering research, ideation, prototype, and LLM/cloud usage
- [ ] Record a narrated video of 5 minutes or less
- [ ] Review and send the submission

## Expected deliverables

- A rapid prototype focused on one insurance workflow or system.
- A short video walkthrough that covers:
  - how I researched the process/system
  - how I approached ideation and requirements gathering
  - a demo of the prototype
  - how I would typically use LLMs and cloud services in a real implementation

## What I think they are evaluating

- Ability to understand an insurance domain problem quickly
- Judgment in choosing a high-value improvement
- Pragmatism in scoping a prototype
- Communication of tradeoffs, assumptions, and architecture
- Ability to make sound engineering decisions under time constraints
- Quality of system design, technical decomposition, and implementation approach
- Comfort using AI/LLMs and cloud services appropriately

## Practical approach

- [x] Focus on death claim intake + next-step orchestration as the chosen life-insurance workflow
- [x] Research the [current-state process, pain points, and operational constraints](plan/death-claim/process-understanding.md)
- [x] Define a target user, problem statement, and success criteria in [plan/death-claim/steel-thread.md](plan/death-claim/steel-thread.md)
- [x] Define the [synthetic data strategy and fixture sources](plan/death-claim/synthetic-data-plan.md) for the chosen workflow
- [x] Shape the prototype as a minimal Lean-Clean steel thread with only the layers, drivers, and adapters needed for the end-to-end slice
  - Current implementation-control docs: [plan/implementation/repo-bootstrap-plan.md](plan/implementation/repo-bootstrap-plan.md), [plan/implementation/tooling-validation-plan.md](plan/implementation/tooling-validation-plan.md), [plan/implementation/acceptance-contract-plan.md](plan/implementation/acceptance-contract-plan.md), [plan/implementation/README.md](plan/implementation/README.md)
- [ ] Add supporting tooling and local infrastructure only where it improves development flow, demoability, or technical credibility
- [ ] Build a thin-slice prototype that clearly shows the improved experience or system behavior
- [ ] Prepare a concise demo narrative that ties together research, requirements, prototype, and technical approach

## Constraints and assumptions

- The prototype does not need to be production-ready.
- The implementation will start from a minimal Lean-Clean steel-thread structure rather than a generic application scaffold.
- `uv`, FastAPI, Ruff, Pyright, Docker, Tilt, and VS Code are baseline tooling choices, but the exact project shape should remain driven by the chosen PoC slice.
- A broader platform-level structure is optional and should only be introduced if it clearly strengthens this PoC.
- The current working shape is a graph-owned triage flow surfaced primarily through an internal claims-ops workbench with three representative case tabs, plus a thin internal API shell and generated external follow-up artifacts.
- Clear reasoning, architecture, and technical execution likely matter more than polish.
- The demo should stay tightly scoped so it fits within 5 minutes.
- The response window is 3-5 business days.

## Likely presentation structure

1. Problem and research summary
2. Pain point and proposed improvement
3. Prototype demo
4. How LLMs and cloud would support a real deployment
5. Key assumptions, risks, and next steps
