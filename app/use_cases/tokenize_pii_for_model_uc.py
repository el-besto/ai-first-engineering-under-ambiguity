from app.adapters.safety.protocol import PIIGuardrailAdapter


class TokenizePIIForModelUseCase:
    def __init__(self, guardrail: PIIGuardrailAdapter):
        self.guardrail = guardrail

    def execute(self, raw_text: str) -> tuple[str, dict]:
        return self.guardrail.tokenize(raw_text)
