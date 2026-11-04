
from app.services.vector_store import search_chunks


def retrieve_relevant_chunks(query: str, top_k: int = 3) -> list[dict]:
    results = search_chunks(query=query, top_k=top_k)
    return results
