from typing import Any, Protocol


class PIIGuardrailAdapter(Protocol):
    """
    Explicit provider-agnostic privacy boundary before any external model call.
    - raw input in
    - tokenized safe text and safe context out
    - reversible token map out
    """

    def tokenize(self, raw_input: str) -> tuple[str, dict[str, Any]]: ...

    def detokenize(self, safe_input: str, token_map: dict[str, Any]) -> str: ...
