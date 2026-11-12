from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.paper import PaperCreate, PaperUpdate, PaperResponse
from app.services import paper_service

from fastapi import UploadFile, File
import pymupdf

from app.services import document_service

router = APIRouter(prefix="/papers", tags=["Papers"])


@router.post("/", response_model=PaperResponse)
def create_paper(
    paper_data: PaperCreate,
    db: Session = Depends(get_db)
):
    return paper_service.create_paper(
        db, paper_data.model_dump()
    )


@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = paper_service.get_paper(db, paper_id)

    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return paper


@router.get("/", response_model=list[PaperResponse])
def get_all_papers(db: Session = Depends(get_db)):
    return paper_service.get_all_papers(db)


@router.put("/{paper_id}", response_model=PaperResponse)
def update_paper(
    paper_id: int,
    update_data: PaperUpdate,
    db: Session = Depends(get_db)
):
    paper = paper_service.update_paper(
        db, paper_id, update_data.model_dump()
    )

    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return paper


@router.delete("/{paper_id}")
def delete_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = paper_service.delete_paper(db, paper_id)

    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return {"message": "Paper deleted successfully"}


@router.post("/{paper_id}/documents", status_code=201)
async def upload_paper_document(
    paper_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
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
    except Exception as exc:
        print(repr(exc))
        raise


    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found.",
        )

    return {
        "id": document.id,
        "paper_id": document.paper_id,
        "filename": document.filename,
        "pages": page_count,
        "status": "uploaded",
    }