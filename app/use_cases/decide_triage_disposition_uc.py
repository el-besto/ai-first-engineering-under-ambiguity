from app.use_cases.protocols import LoggerProtocol


class DecideTriageDispositionUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, is_complete: bool, is_ambiguous: bool) -> tuple[str, str]:
        self.logger.info("started")
        if is_ambiguous:
            self.logger.info("completed", disposition="escalate_to_human_review", confidence="Low")
            return "escalate_to_human_review", "Low"
        if is_complete:
            self.logger.info("completed", disposition="proceed", confidence="High")
            return "proceed", "High"

        self.logger.info("completed", disposition="request_more_information", confidence="Medium")
        return "request_more_information", "Medium"
