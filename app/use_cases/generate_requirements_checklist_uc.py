class GenerateRequirementsChecklistUseCase:
    def execute(self, document_facts: dict) -> str:
        required_docs = {"CUSTOMER_REQUEST", "POLICY_SUMMARY", "CLAIM_INTAKE_FORM"}
        present_docs = set(document_facts.get("documents_present", []))
        missing_docs = required_docs - present_docs
        missing_fields = document_facts.get("missing_fields", [])

        if not missing_docs and not missing_fields:
            return ""

        checklist = "Missing Information:\n"
        for doc in missing_docs:
            checklist += f"- {doc}\n"
        for field in missing_fields:
            checklist += f"- {field}\n"

        return checklist
