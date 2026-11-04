from app.services.pdf_loader import extract_pages, chunk_pages
from app.services.vector_store import add_chunks, collection
from app.services.vector_store import search_chunks

pdf_path = "data/Building Effective AI Agents.pdf"

pages = extract_pages(pdf_path)
chunks = chunk_pages(pages)

add_chunks(chunks, source="Building Effective AI Agents.pdf")

result = collection.get(
    where={"source": "Building Effective AI Agents.pdf"},
    include=["documents", "metadatas"],
)

print("Pages:", len(pages))
print("Generated chunks:", len(chunks))
print("Stored chunks:", len(result["ids"]))
print("First stored chunk:", result["documents"][0])
print("First metadata:", result["metadatas"][0])

results = search_chunks("How do AI agents use tools?")

for result in results:
    print("Page:", result["metadata"]["page_number"])
    print("Text:", result["text"][:200])
    print("-" * 40)
