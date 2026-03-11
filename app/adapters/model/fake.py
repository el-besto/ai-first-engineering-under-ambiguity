from app.adapters.model.protocol import ModelAdapter


class FakeModelAdapter(ModelAdapter):
    def generate(self, prompt: str) -> str:
        if "checklist" in prompt.lower():
            return "Fake Checklist"
        elif "message" in prompt.lower():
            return "Fake Message"
        elif "rationale" in prompt.lower():
            return "Fake Rationale"
        elif "summary" in prompt.lower():
            return "Fake Summary"
        return "Fake Generated Output"
