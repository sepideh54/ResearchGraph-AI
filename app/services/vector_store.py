
import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(name="research_chunks")

def add_chunks(chunks: list[dict], source: str) -> None:
    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        ids.append(f"{source}_page_{chunk['page_number']}_chunk_{index}")
        documents.append(chunk["text"])
        metadatas.append({
            "source": source,
            "page_number": chunk["page_number"],
            "chunk_index": index,
        })

    if ids:
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )


def search_chunks(query: str, top_k: int = 3) -> list[dict]:
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    chunks = []

    for i, text in enumerate(results["documents"][0]):
        chunks.append({
            "text": text,
            "metadata": results["metadatas"][0][i],
        })

    return chunks
