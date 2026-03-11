from pydantic import BaseModel, Field


class CaseSummaryModel(BaseModel):
    summary_text: str


class RoutingDecisionModel(BaseModel):
    target_queue: str
    rationale: str


class DeathClaimResponse(BaseModel):
    disposition: str
    confidence_band: str
    case_summary: CaseSummaryModel | None = None
    routing_decision: RoutingDecisionModel | None = None
    requirements_checklist: str | None = None
    follow_up_message: str | None = None
    follow_up_message_quality_markers: list[str] = Field(default_factory=list)
    hitl_review_task: str | None = None
    reviewability_flags: list[str] = Field(default_factory=list)
    escalation_reasons: list[str] = Field(default_factory=list)
    escalation_rationale: str | None = None
