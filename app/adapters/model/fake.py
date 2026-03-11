from app.adapters.model.protocol import ModelAdapter
from app.infrastructure.telemetry.logger import get_logger


class FakeModelAdapter(ModelAdapter):
    def __init__(self):
        self.logger = get_logger(__name__).bind(adapter=self.__class__.__name__)

    def generate(self, prompt: str) -> str:
        log = self.logger.bind(operation="generate")
        log.info("started", prompt_chars=len(prompt))
        if "generate a list of missing requirements" in prompt:
            response = '{"reasoning": "Fake reasoning", "missing_items": ["Fake item 1", "Fake item 2"]}'
        elif "draft a follow-up message" in prompt:
            response = (
                '{"reasoning": "Fake reasoning", '
                '"message": "Fake Message", '
                '"quality_markers": ["empathetic", "clear", "non-adjudicative"]}'
            )
        elif "internal routing rationale" in prompt:
            response = '{"reasoning": "Fake reasoning", "rationale": "Fake Rationale"}'
        elif "concise summary of the facts" in prompt:
            response = '{"reasoning": "Fake reasoning", "summary": "Fake Summary"}'
        elif "task description for a human-in-the-loop" in prompt:
            response = '{"reasoning": "Fake reasoning", "task_description": "Fake Task Description"}'
        else:
            response = '{"reasoning": "Fake reasoning", "output": "Fake Generated Output"}'

        log.info("completed", response_chars=len(response))
        return response
