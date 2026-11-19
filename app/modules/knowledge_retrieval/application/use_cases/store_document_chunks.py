
from app.services.pdf_loader import chunk_pages
from app.services.semantic_search import embed_chunks
from app.services.schemas import PageData

from app.modules.knowledge_retrieval.application.ports.document_chunk_repository import (
    DocumentChunkRepository,
)


class StoreDocumentChunks:

    def __init__(self, repository: DocumentChunkRepository):
        self.repository = repository

    def execute(
        self,
        document_id: int,
        pages: list[PageData],
    ) -> int:

        try:
            chunks = chunk_pages(pages)

            if not chunks:
                self.repository.delete_by_document_id(document_id)
                self.repository.commit()
                return 0

            embedded_chunks = embed_chunks(chunks)

            self.repository.delete_by_document_id(document_id)

            self.repository.save_many(
                document_id=document_id,
                chunks=embedded_chunks,
            )

            self.repository.commit()

            return len(embedded_chunks)

        except Exception:
            self.repository.rollback()
            raise
