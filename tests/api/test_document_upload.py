
import pymupdf
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.db.session import get_db
from app.api.dependencies import get_store_document_chunks
from app.models.paper import Paper
from app.models.document import Document
from app.services import document_service


class FakeStoreDocumentChunks:
    def execute(self, document_id, pages):
        return 2


class FailingStoreDocumentChunks:
    def execute(self, document_id, pages):
        raise RuntimeError("Embedding service failed")


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_store_document_chunks] = (
        lambda: FakeStoreDocumentChunks()
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def valid_pdf():
    pdf = pymupdf.open()
    pdf.new_page()
    content = pdf.tobytes()
    pdf.close()
    return content


@pytest.fixture
def paper(db_session):
    paper = Paper(title="Test Research Paper")
    db_session.add(paper)
    db_session.flush()
    return paper


def test_upload_document_success(
    client, db_session, paper, valid_pdf, monkeypatch, tmp_path
):
    monkeypatch.setattr(document_service, "STORAGE_DIR", tmp_path)

    response = client.post(
        f"/papers/{paper.id}/documents",
        files={"file": ("test.pdf", valid_pdf, "application/pdf")},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "completed"
    assert response.json()["chunks"] == 2

    document = db_session.query(Document).one()
    assert document.status == "completed"


def test_reject_non_pdf_file(client):
    response = client.post(
        "/papers/1/documents",
        files={"file": ("test.txt", b"some text", "text/plain")},
    )

    assert response.status_code == 400


def test_upload_to_nonexistent_paper(
    client, valid_pdf, monkeypatch, tmp_path
):
    monkeypatch.setattr(document_service, "STORAGE_DIR", tmp_path)

    response = client.post(
        "/papers/999999/documents",
        files={"file": ("test.pdf", valid_pdf, "application/pdf")},
    )

    assert response.status_code == 404


def test_processing_failure_marks_document_failed(
    client, db_session, paper, valid_pdf, monkeypatch, tmp_path
):
    monkeypatch.setattr(document_service, "STORAGE_DIR", tmp_path)

    app.dependency_overrides[get_store_document_chunks] = (
        lambda: FailingStoreDocumentChunks()
    )

    response = client.post(
        f"/papers/{paper.id}/documents",
        files={"file": ("test.pdf", valid_pdf, "application/pdf")},
    )

    assert response.status_code == 500

    document = db_session.query(Document).one()
    assert document.status == "failed"
    assert "Embedding service failed" in document.processing_error

def test_retry_document_not_found(client):
    response = client.post("/papers/documents/99999/retry")

    assert response.status_code == 404


def test_retry_document_rejects_non_failed_status(
    client, db_session, paper
):
    document = Document(
        paper_id=paper.id,
        filename="sample.pdf",
        file_path="sample.pdf",
        status="completed",
    )
    db_session.add(document)
    db_session.commit()

    response = client.post(
        f"/papers/documents/{document.id}/retry"
    )

    assert response.status_code == 409


def test_retry_document_success(
    client, db_session, paper, valid_pdf, tmp_path
):
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(valid_pdf)

    document = Document(
        paper_id=paper.id,
        filename="sample.pdf",
        file_path=str(pdf_path),
        status="failed",
        processing_error="Previous processing failed",
    )
    db_session.add(document)
    db_session.commit()

    response = client.post(
        f"/papers/documents/{document.id}/retry"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["chunks"] == 2

    db_session.refresh(document)
    assert document.status == "completed"
    assert document.processing_error is None