from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.use_cases.protocols import LoggerProtocol


class TokenizePIIForModelUseCase:
    def __init__(self, guardrail: PIIGuardrailAdapter, logger: LoggerProtocol):
        self.guardrail = guardrail
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, raw_text: str) -> tuple[str, dict]:
        self.logger.info("started")
        result = self.guardrail.tokenize(raw_text)
        self.logger.info("completed", tokens_generated=len(result[1]))
        return result
