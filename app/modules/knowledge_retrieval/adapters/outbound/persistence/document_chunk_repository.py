
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.knowledge_retrieval.application.ports.document_chunk_repository import (
    DocumentChunkRepository,
)
from app.modules.knowledge_retrieval.adapters.outbound.persistence.document_chunk import (
    DocumentChunk,
)


class PostgreSQLDocumentChunkRepository(DocumentChunkRepository):

    def __init__(self, db: Session):
        self.db = db

    def save_many(
        self,
        document_id: int,
        chunks: list[dict],
    ) -> None:
        records = [
            DocumentChunk(
                document_id=document_id,
                page_number=chunk["page_number"],
                chunk_index=chunk["chunk_index"],
                text=chunk["text"],
                embedding=chunk["embedding"],
            )
            for chunk in chunks
        ]
        self.db.add_all(records)

    def delete_by_document_id(self, document_id: int) -> None:
        self.db.query(DocumentChunk).filter(
              DocumentChunk.document_id == document_id
        ).delete(synchronize_session=False)
    
    def search_similar(
        self,
        query_embedding: list[float],
        limit: int = 5,
        document_id: int | None = None,
    ) -> list[dict]:
        distance = DocumentChunk.embedding.cosine_distance(query_embedding)

        statement = select(
            DocumentChunk,
            distance.label("distance"),
        )

        if document_id is not None:
            statement = statement.where(
                DocumentChunk.document_id == document_id
            )

        statement = statement.order_by(distance).limit(limit)
        results = self.db.execute(statement).all()

        return [
            {
                "id": chunk.id,
                "document_id": chunk.document_id,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
                "distance": float(distance_value),
            }
            for chunk, distance_value in results
        ]

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
