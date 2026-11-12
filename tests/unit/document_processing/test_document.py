import pytest

from app.modules.document_processing.domain.document import (
    Document,
    DocumentStatus,
)


def create_document(**overrides):
    data = {
        "id": 1,
        "paper_id": 10,
        "original_filename": "research.pdf",
        "storage_key": "documents/abc123.pdf",
        "content_type": "application/pdf",
        "size_bytes": 1024,
        "checksum_sha256": "a" * 64,
    }
    data.update(overrides)
    return Document(**data)


def test_create_document():
    document = create_document()

    assert document.id == 1
    assert document.paper_id == 10
    assert document.status == DocumentStatus.STORED


def test_reject_invalid_paper_id():
    with pytest.raises(ValueError):
        create_document(paper_id=0)


def test_reject_empty_filename():
    with pytest.raises(ValueError):
        create_document(original_filename="   ")


def test_reject_empty_storage_key():
    with pytest.raises(ValueError):
        create_document(storage_key="   ")


def test_reject_non_pdf_file():
    with pytest.raises(ValueError):
        create_document(content_type="image/png")


def test_reject_invalid_file_size():
    with pytest.raises(ValueError):
        create_document(size_bytes=0)


def test_reject_invalid_checksum():
    with pytest.raises(ValueError):
        create_document(checksum_sha256="invalid")


def test_trash_document():
    document = create_document()

    document.trash()

    assert document.status == DocumentStatus.TRASHED


def test_restore_document():
    document = create_document()
    document.trash()

    document.restore()

    assert document.status == DocumentStatus.STORED


def test_cannot_trash_document_twice():
    document = create_document()
    document.trash()

    with pytest.raises(ValueError):
        document.trash()


def test_cannot_restore_stored_document():
    document = create_document()

    with pytest.raises(ValueError):
        document.restore()