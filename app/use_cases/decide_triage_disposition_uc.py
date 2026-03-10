class DecideTriageDispositionUseCase:
    def execute(self, is_complete: bool) -> tuple[str, str]:
        if is_complete:
            return "proceed", "High"
        return "request_more_information", "Medium"
