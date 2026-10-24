from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
def create_embeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings

def create_embeddings(chunks):
    embeddings = model.encode(chunks, normalize_embeddings=True)
    return embeddings

# def find_most_relevant(query, chunks):
#     chunk_embeddings = model.encode(chunks, normalize_embeddings=True)
#     query_embedding = model.encode(query, normalize_embeddings=True)

#     scores = chunk_embeddings @ query_embedding.T
#     best_index = scores.argmax()

#     return chunks[best_index], float(scores[best_index])
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