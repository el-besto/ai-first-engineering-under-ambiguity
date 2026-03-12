from app.use_cases.protocols import LoggerProtocol


class GenerateEscalationRationaleUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, document_facts: dict) -> tuple[list[str], str]:
        self.logger.info("started")
        reasons = ["Ambiguous Date of Death vs Policy Active Date"]
        rationale = "The documents contain inconsistencies requiring human review. No decision has been made."
        self.logger.info("completed", escalation_reason_count=len(reasons))
        return reasons, rationale
