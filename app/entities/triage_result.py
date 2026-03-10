from dataclasses import dataclass, field

from app.entities.case_summary import CaseSummary
from app.entities.routing_decision import RoutingDecision


@dataclass(slots=True, frozen=True)
class TriageResult:
    disposition: str
    confidence_band: str
    case_summary: CaseSummary | None = None
    routing_decision: RoutingDecision | None = None
    requirements_checklist: str | None = None
    follow_up_message: str | None = None
    follow_up_message_quality_markers: list[str] = field(default_factory=list)
    hitl_review_task: str | None = None
    reviewability_flags: list[str] = field(default_factory=list)
    escalation_reasons: list[str] = field(default_factory=list)
    escalation_rationale: str | None = None
