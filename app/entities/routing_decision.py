from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RoutingDecision:
    target_queue: str
    rationale: str
