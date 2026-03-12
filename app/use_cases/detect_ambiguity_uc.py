from app.use_cases.protocols import LoggerProtocol


class DetectAmbiguityUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, document_facts: dict) -> bool:
        self.logger.info("started")
        # For this slice, any case with a DEATH_CERTIFICATE is treated as ambiguous (Case C)
        # We will expand this in Slice 6. For now, it just isolates Case C from Case A/B.
        present = set(document_facts.get("documents_present", []))
        result = "DEATH_CERTIFICATE" in present
        self.logger.info("completed", is_ambiguous=result)
        return result
