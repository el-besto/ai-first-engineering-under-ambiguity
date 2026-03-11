from typing import Protocol


class ModelAdapter(Protocol):
    def generate(self, prompt: str) -> str: ...
