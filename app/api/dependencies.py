from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.knowledge_retrieval.adapters.outbound.persistence.document_chunk_repository import (
    PostgreSQLDocumentChunkRepository,
)

from app.modules.knowledge_retrieval.application.use_cases.store_document_chunks import (
    StoreDocumentChunks,
)


def get_store_document_chunks(
    db: Session = Depends(get_db),
) -> StoreDocumentChunks:

    repository = PostgreSQLDocumentChunkRepository(db)

    return StoreDocumentChunks(repository)