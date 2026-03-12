from typing import Any

from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.use_cases.protocols import LoggerProtocol


class ExtractDocumentFactsUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, bundle: ClaimIntakeBundle) -> dict[str, Any]:
        self.logger.info("started", document_count=len(bundle.documents))
        facts: dict[str, Any] = {"documents_present": list(bundle.documents.keys())}
        missing_fields = []

        if "CLAIM_INTAKE_FORM" in bundle.documents:
            form_text = bundle.documents["CLAIM_INTAKE_FORM"]
            if "[MISSING]" in form_text:
                missing_fields.append("Signature")
            # TODO: DEFERRED - Replace regex mocked extraction with robust structured ingestion
            # (e.g., Unstructured, Docling) or an LLM extraction model.
            # Simple regex/split extraction for the sake of end-to-end tests
            import re

            claimant_match = re.search(r"Claimant Name:\s*(.*)", form_text)
            if claimant_match:
                facts["claimant_name"] = claimant_match.group(1).strip()

            deceased_match = re.search(r"Deceased Name:\s*(.*)", form_text)
            if deceased_match:
                facts["deceased_name"] = deceased_match.group(1).strip()

        facts["missing_fields"] = missing_fields
        facts["document_texts"] = bundle.documents
        self.logger.info("completed", extracted_fields=list(facts.keys()))
        return facts
