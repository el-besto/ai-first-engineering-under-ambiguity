# Death-Claim Deferred Hardening Items

> **Purpose:** Track the known unknowns that are intentionally deferred while the death-claim scenario is translated into downstream structural artifacts.

---

**Status:** Active PoC planning artifact

This file exists to make the current deferments explicit. These are not accidental omissions. They are bounded hardening items with clear triggers.

| Defer item                                       | Reason                                                                                                                                                                              | Hardening trigger                                                                                                               |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| Exact missing-vs-ambiguous boundary              | The workshop spec proves the three-case pattern, but the precise disposition boundary still needs claims-ops and governance alignment before it becomes architecture-driving logic. | Before the scenario is translated into concrete routing or escalation rules in the vertical slice or downstream Tree A example. |
| Exact tone markers for claimant-facing follow-up | The workshop spec establishes empathy and operational appropriateness, but not the final review rubric for claimant-facing language.                                                | Before follow-up-message prompts, templates, or review criteria are treated as stable demo behavior.                            |
| Exact governance/data-science review metrics     | The workshop spec requires inspectability, but does not yet lock the scorecard or demo review signals.                                                                              | Before eval, observability, or demo instrumentation are treated as acceptance-driving outputs.                                  |
| Exact confidence/reviewability model             | The scenario now needs an explicit reviewability signal, but the final rubric, weighting, and thresholds are not yet hardened.                                                      | Before confidence/reviewability is treated as a stable acceptance or demo-governing output.                                     |
