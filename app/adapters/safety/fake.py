from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.infrastructure.telemetry.logger import get_logger


class FakePIIGuardrail(PIIGuardrailAdapter):
    def __init__(self):
        self._tokenizer_called = False
        self.logger = get_logger(__name__).bind(adapter=self.__class__.__name__)

    def tokenize(self, raw_input: str) -> tuple[str, dict]:
        log = self.logger.bind(operation="tokenize")
        log.debug("started", input_chars=len(raw_input))
        self._tokenizer_called = True
        log.debug("completed", token_count=0)
        return raw_input, {}

    def detokenize(self, safe_input: str, token_map: dict) -> str:
        self.logger.bind(operation="detokenize").debug("completed", token_count=len(token_map))
        return safe_input

    def external_model_input_contains_no_raw_pii(self) -> bool:
        return self._tokenizer_called

    def used_stable_safe_tokens(self) -> bool:
        return self._tokenizer_called
