from app.use_cases.protocols import LoggerProtocol


class GenerateHITLReviewTaskUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, document_facts: dict) -> str:
        self.logger.info("started")
        task = "Review ambiguous death certificate and compare with policy terms."
        self.logger.info("completed", task_generated=True)
        return task
