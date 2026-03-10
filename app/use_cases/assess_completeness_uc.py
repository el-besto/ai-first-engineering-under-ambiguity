class AssessCompletenessUseCase:
    def execute(self, document_facts: dict) -> bool:
        required = {"CUSTOMER_REQUEST", "POLICY_SUMMARY", "CLAIM_INTAKE_FORM"}
        present = set(document_facts.get("documents_present", []))
        return required.issubset(present)
