from app.adapters.model.protocol import ModelAdapter


class FakeModelAdapter(ModelAdapter):
    def generate(self, prompt: str) -> str:
        if "generate a list of missing requirements" in prompt:
            return '{"reasoning": "Fake reasoning", "missing_items": ["Fake item 1", "Fake item 2"]}'
        elif "draft a follow-up message" in prompt:
            return (
                '{"reasoning": "Fake reasoning", '
                '"message": "Fake Message", '
                '"quality_markers": ["empathetic", "clear", "non-adjudicative"]}'
            )
        elif "internal routing rationale" in prompt:
            return '{"reasoning": "Fake reasoning", "rationale": "Fake Rationale"}'
        elif "concise summary of the facts" in prompt:
            return '{"reasoning": "Fake reasoning", "summary": "Fake Summary"}'
        elif "task description for a human-in-the-loop" in prompt:
            return '{"reasoning": "Fake reasoning", "task_description": "Fake Task Description"}'
        return '{"reasoning": "Fake reasoning", "output": "Fake Generated Output"}'
