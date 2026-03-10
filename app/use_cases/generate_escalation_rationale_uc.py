class GenerateEscalationRationaleUseCase:
    def execute(self, document_facts: dict) -> tuple[list[str], str]:
        reasons = ["Ambiguous Date of Death vs Policy Active Date"]
        rationale = (
            "The documents contain inconsistencies requiring human review. "
            "No decision has been made."
        )
        return reasons, rationale
