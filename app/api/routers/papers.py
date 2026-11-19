
from pathlib import Path

import pymupdf
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.api.dependencies import get_store_document_chunks
from app.db.session import get_db
from app.models.document import Document
from app.schemas.paper import PaperCreate, PaperUpdate, PaperResponse
from app.services import paper_service, document_service
from app.services.pdf_loader import extract_pages
from app.modules.knowledge_retrieval.application.use_cases.store_document_chunks import (
    StoreDocumentChunks,
)


router = APIRouter(prefix="/papers", tags=["Papers"])


@router.post("/", response_model=PaperResponse)
def create_paper(
    paper_data: PaperCreate,
    db: Session = Depends(get_db),
):
    return paper_service.create_paper(
        db, paper_data.model_dump()
    )


@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
):
    paper = paper_service.get_paper(db, paper_id)

    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return paper


@router.get("/", response_model=list[PaperResponse])
def get_all_papers(
    db: Session = Depends(get_db),
):
    return paper_service.get_all_papers(db)


@router.put("/{paper_id}", response_model=PaperResponse)
def update_paper(
    paper_id: int,
    update_data: PaperUpdate,
    db: Session = Depends(get_db),
):
    paper = paper_service.update_paper(
        db, paper_id, update_data.model_dump()
    )

    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return paper


@router.delete("/{paper_id}")
def delete_paper(
    paper_id: int,
    db: Session = Depends(get_db),
):
    paper = paper_service.delete_paper(db, paper_id)

    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return {"message": "Paper deleted successfully"}


@router.post("/{paper_id}/documents", status_code=201)
async def upload_paper_document(
    paper_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    store_chunks: StoreDocumentChunks = Depends(get_store_document_chunks),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    try:
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            page_count = len(pdf)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file.",
        )

    try:
        document = document_service.upload_document(
            db=db,
            paper_id=paper_id,
            filename=file.filename,
            content=content,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Document upload failed.",
        )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found.",
        )

    try:
        document.status = "processing"
        document.processing_error = None
        db.commit()

        pages = extract_pages(content)

        chunk_count = store_chunks.execute(
            document_id=document.id,
            pages=pages,
        )

        document.status = "completed"
        document.processing_error = None
        db.commit()

    except Exception as exc:
        db.rollback()

        document = db.get(Document, document.id)
        document.status = "failed"
        document.processing_error = str(exc)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        raise HTTPException(
            status_code=500,
            detail="Document processing failed.",
        )

    return {
        "id": document.id,
        "paper_id": document.paper_id,
        "filename": document.filename,
        "pages": page_count,
        "status": document.status,
        "chunks": chunk_count,
    }


@router.post("/documents/{document_id}/retry")
def retry_document(
    document_id: int,
    db: Session = Depends(get_db),
    store_chunks: StoreDocumentChunks = Depends(get_store_document_chunks),
):
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    if document.status != "failed":
        raise HTTPException(
            status_code=409,
            detail="Only failed documents can be retried",
        )

    try:
        document.status = "processing"
        document.processing_error = None
        db.commit()

        file_path = Path(document.file_path)

        if not file_path.exists():
            raise FileNotFoundError("Stored PDF file not found")

        pages = extract_pages(file_path)

        chunk_count = store_chunks.execute(
            document_id=document.id,
            pages=pages,
        )

        document.status = "completed"
        document.processing_error = None
        db.commit()

        return {
            "document_id": document.id,
            "status": document.status,
            "chunks": chunk_count,
        }

    except Exception as exc:
        db.rollback()

        document = db.get(Document, document_id)

        if document is not None:
            document.status = "failed"
            document.processing_error = str(exc)

            try:
                db.commit()
            except Exception:
                db.rollback()
                raise

        raise HTTPException(
            status_code=500,
            detail="Document retry failed",
        )

    
