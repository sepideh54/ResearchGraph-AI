from app.services.pdf_loader import extract_pages, chunk_pages
from app.services.semantic_search import embed_chunks


if __name__ == "__main__":

    pages = extract_pages("data/Building Effective AI Agents.pdf")
    chunks = chunk_pages(pages)
    embedded_chunks = embed_chunks(chunks)

    print("Chunks:", len(chunks))
    print("Embedded chunks:", len(embedded_chunks))
    print("Embedding dimensions:", len(embedded_chunks[0]["embedding"]))