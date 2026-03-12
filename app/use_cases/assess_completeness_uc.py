from app.use_cases.protocols import LoggerProtocol


class AssessCompletenessUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, document_facts: dict) -> bool:
        self.logger.info("started")
        required_docs = {"CUSTOMER_REQUEST", "POLICY_SUMMARY", "CLAIM_INTAKE_FORM"}
        present_docs = set(document_facts.get("documents_present", []))

        has_all_docs = required_docs.issubset(present_docs)
        has_no_missing_fields = len(document_facts.get("missing_fields", [])) == 0

        self.logger.info("completed")
        return has_all_docs and has_no_missing_fields
