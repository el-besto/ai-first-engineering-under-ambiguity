from app.adapters.safety.protocol import PIIGuardrailAdapter


class FakePIIGuardrail(PIIGuardrailAdapter):
    def tokenize(self, raw_input: str) -> tuple[str, dict]:
        return raw_input, {}

    def detokenize(self, safe_input: str, token_map: dict) -> str:
        return safe_input
