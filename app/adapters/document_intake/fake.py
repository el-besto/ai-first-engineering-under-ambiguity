from app.adapters.document_intake.protocol import DocumentStoreProtocol


class FakeDocumentStore(DocumentStoreProtocol):
    def get_document(self, document_id: str) -> str:
        return ""
