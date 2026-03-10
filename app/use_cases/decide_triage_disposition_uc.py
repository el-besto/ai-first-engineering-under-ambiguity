class DecideTriageDispositionUseCase:
    def execute(self, is_complete: bool, is_ambiguous: bool) -> tuple[str, str]:
        if is_ambiguous:
            return "escalate_to_human_review", "Low"
        if is_complete:
            return "proceed", "High"
        return "request_more_information", "Medium"
