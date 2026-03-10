from app.entities.claim_intake_bundle import ClaimIntakeBundle


class ExtractDocumentFactsUseCase:
    def execute(self, bundle: ClaimIntakeBundle) -> dict:
        facts = {"documents_present": list(bundle.documents.keys())}
        missing_fields = []

        if "CLAIM_INTAKE_FORM" in bundle.documents:
            form_text = bundle.documents["CLAIM_INTAKE_FORM"]
            if "[MISSING]" in form_text:
                missing_fields.append("Signature")

        facts["missing_fields"] = missing_fields
        return facts
