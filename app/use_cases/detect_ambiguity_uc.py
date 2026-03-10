class DetectAmbiguityUseCase:
    def execute(self, document_facts: dict) -> bool:
        # For this slice, any case with a DEATH_CERTIFICATE is treated as ambiguous (Case C)
        # We will expand this in Slice 6. For now, it just isolates Case C from Case A/B.
        present = set(document_facts.get("documents_present", []))
        return "DEATH_CERTIFICATE" in present
