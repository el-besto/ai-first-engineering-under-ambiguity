from app.use_cases.protocols import LoggerProtocol


class GenerateRequirementsChecklistUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, document_facts: dict) -> str:
        self.logger.info("started")
        required_docs = {"CUSTOMER_REQUEST", "POLICY_SUMMARY", "CLAIM_INTAKE_FORM"}
        present_docs = set(document_facts.get("documents_present", []))
        missing_docs = required_docs - present_docs
        missing_fields = document_facts.get("missing_fields", [])

        if not missing_docs and not missing_fields:
            self.logger.info("completed", checklist_generated=False)
            return ""

        checklist = "Missing Information:\n"
        for doc in missing_docs:
            checklist += f"- {doc}\n"
        for field in missing_fields:
            checklist += f"- {field}\n"

        self.logger.info(
            "completed",
            checklist_generated=True,
            missing_items_count=len(missing_docs) + len(missing_fields),
        )
        return checklist
