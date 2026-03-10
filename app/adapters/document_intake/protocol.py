from typing import Protocol


class DocumentStoreProtocol(Protocol):
    def get_document(self, document_id: str) -> str: ...
