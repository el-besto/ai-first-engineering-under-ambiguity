from app.use_cases.protocols import LoggerProtocol


class GenerateFollowUpMessageUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, checklist: str) -> tuple[str, list[str]]:
        self.logger.info("started")
        if not checklist:
            self.logger.info("completed", message_generated=False)
            return "", []

        message = (
            "We are very sorry for your loss. "
            "To help us process this claim, please provide the following "
            f"information:\n{checklist}"
        )

        quality_markers = ["empathetic", "clear", "non-adjudicative"]
        self.logger.info("completed", message_generated=True, quality_markers=quality_markers)
        return message, quality_markers
