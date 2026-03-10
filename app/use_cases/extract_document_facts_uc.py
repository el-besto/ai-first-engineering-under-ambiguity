from app.entities.claim_intake_bundle import ClaimIntakeBundle


class ExtractDocumentFactsUseCase:
    def execute(self, bundle: ClaimIntakeBundle) -> dict:
        # Simplest structural stub for extraction
        return {"documents_present": list(bundle.documents.keys())}
