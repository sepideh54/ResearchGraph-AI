
from abc import ABC, abstractmethod


class DocumentChunkRepository(ABC):

    @abstractmethod
    def save_many(
        self,
        document_id: int,
        chunks: list[dict],
    ) -> None:
        pass

    @abstractmethod
    def search_similar(
        self,
        query_embedding: list[float],
        limit: int = 5,
        document_id: int | None = None,
    ) -> list[dict]:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def delete_by_document_id(self, document_id: int) -> None:
       pass