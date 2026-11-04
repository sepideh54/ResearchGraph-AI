from app.services.pdf_loader import extract_pages
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import pymupdf
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db

app = FastAPI(
    title="ResearchGraph AI",
    description="A multi-stage RAG system for research literature",
    version="0.1.0",
)

@app.get("/db-health")
def check_database(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {
        "database": "connected",
        "result": result.scalar()
    }


@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted.",
        )

    content = await file.read()
    pages = extract_pages(content)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    try:
        with pymupdf.open(stream=content, filetype="pdf") as document:
            page_count = len(document)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF.",
        )

    return {
        "filename": file.filename,
        "pages": len(pages),
        "status": "validated",
    }
