from app.adapters.safety.protocol import PIIGuardrailAdapter


class FakePIIGuardrail(PIIGuardrailAdapter):
    def __init__(self):
        self._tokenizer_called = False

    def tokenize(self, raw_input: str) -> tuple[str, dict]:
        self._tokenizer_called = True
        return raw_input, {}

    def detokenize(self, safe_input: str, token_map: dict) -> str:
        return safe_input

    def external_model_input_contains_no_raw_pii(self) -> bool:
        return self._tokenizer_called

    def used_stable_safe_tokens(self) -> bool:
        return self._tokenizer_called
