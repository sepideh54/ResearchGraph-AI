import pymupdf
from app.services.schemas import PageData
from pathlib import Path

def extract_pages(source: bytes | str | Path) -> list[PageData]:
    if isinstance(source, bytes):
        doc = pymupdf.open(stream=source, filetype="pdf")
    else:
        doc = pymupdf.open(source)

    with doc:
        pages = []

        for page_number, page in enumerate(doc, start=1):
            page_data = PageData(
                page_number=page_number,
                text=page.get_text(),
            )
            pages.append(page_data)
    return pages


def chunk_pages(pages: list[PageData], chunk_size: int = 100, overlap: int = 20) -> list[dict]:
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    step = chunk_size - overlap

    for page in pages:
        words = page.text.split()

        for start in range(0, len(words), step):
            chunk_words = words[start:start + chunk_size]

            if not chunk_words:
                continue

            chunks.append({
                "text": " ".join(chunk_words),
                "page_number": page.page_number,
            })

    return chunks

if __name__ == "__main__":
    pages = extract_pages("data/Building Effective AI Agents.pdf")
    chunks = chunk_pages(pages)

    print("Total pages:", len(pages))
    print("Total chunks:", len(chunks))
    print("First chunk:", chunks[0])


