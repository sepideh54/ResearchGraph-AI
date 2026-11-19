#تبدیل متن به بردار عددی (Embedding) و جست‌وجوی معنایی (Semantic Search) است.
#بعداً مسئولیت‌هایش را به ماژول‌های knowledge_processing و knowledge_retrieval منتقل می‌کنیم.

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def create_embeddings(chunks, batch_size=32):
    embeddings = model.encode(
        chunks,
        batch_size=batch_size,
        normalize_embeddings=True
    )
    return embeddings

def search_chunks(query, chunks, chunk_embeddings, top_k=3):
    query_embedding = model.encode(query, normalize_embeddings=True)

    scores = chunk_embeddings @ query_embedding.T
    best_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in best_indices:
        results.append((chunks[index], float(scores[index])))

    return results

def save_embeddings(embeddings, path="data/embeddings.npy"):
    np.save(path, embeddings)


def load_embeddings(path="data/embeddings.npy"):
    return np.load(path)

def retrieve_relevant_chunks(query, chunks, chunk_embeddings, top_k=3):
    results = search_chunks(
        query,
        chunks,
        chunk_embeddings,
        top_k=top_k
    )
    return results

def embed_chunks(chunks: list[dict]) -> list[dict]:
    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]

    embeddings = create_embeddings(texts)

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            **chunk,
            "embedding": embedding.tolist(),
        })

    return embedded_chunks