import pymupdf
import pytest

from app.services.pdf_loader import chunk_pages, extract_pages
from app.services.schemas import PageData


def make_pdf_bytes(text: str) -> bytes:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def test_extract_pages_from_pdf_bytes_preserves_page_number_and_text():
    pages = extract_pages(make_pdf_bytes("Research evidence"))

    assert len(pages) == 1
    assert pages[0].page_number == 1
    assert "Research evidence" in pages[0].text


def test_chunk_pages_preserves_page_number_and_applies_overlap():
    pages = [
        PageData(page_number=3, text="one two three four five six seven")
    ]

    chunks = chunk_pages(pages, chunk_size=4, overlap=1)

    assert [chunk["text"] for chunk in chunks] == [
        "one two three four",
        "four five six seven",
        "seven",
    ]
    assert all(chunk["page_number"] == 3 for chunk in chunks)


@pytest.mark.parametrize(
    ("chunk_size", "overlap"),
    [(0, 0), (4, -1), (4, 4)],
)
def test_chunk_pages_rejects_invalid_chunk_configuration(
    chunk_size: int,
    overlap: int,
):
    pages = [PageData(page_number=1, text="some text")]

    with pytest.raises(ValueError, match="overlap must be smaller than chunk_size"):
        chunk_pages(pages, chunk_size=chunk_size, overlap=overlap)


def test_chunk_pages_returns_empty_list_for_empty_page():
    pages = [PageData(page_number=1, text="")]

    assert chunk_pages(pages) == []
