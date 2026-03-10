class GenerateFollowUpMessageUseCase:
    def execute(self, checklist: str) -> tuple[str, list[str]]:
        if not checklist:
            return "", []

        message = (
            "We are very sorry for your loss. "
            "To help us process this claim, please provide the following "
            f"information:\n{checklist}"
        )

        quality_markers = ["empathetic", "clear", "non-adjudicative"]
        return message, quality_markers
