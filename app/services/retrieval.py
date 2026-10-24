from app.services.pdf_loader import chunk_text,extract
from app.services.semantic_search import save_embeddings,create_embeddings,search_chunks

def retrieve_from_pdf(pdf_path, query, top_k=3):
    text = extract(pdf_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    results = search_chunks(query, chunks, embeddings, top_k=top_k)
    return results
