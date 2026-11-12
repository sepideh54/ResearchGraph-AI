from pathlib import Path
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.paper import Paper


STORAGE_DIR = Path("data/documents")


def upload_document(
    db: Session,
    paper_id: int,
    filename: str,
    content: bytes,
):
    paper = db.get(Paper, paper_id)

    if paper is None:
        return None

    stored_path = STORAGE_DIR / f"{uuid4().hex}.pdf"

    try:
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        stored_path.write_bytes(content)

        document = Document(
            paper_id=paper_id,
            filename=Path(filename.replace("\\", "/")).name,
            file_path=str(stored_path),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    except Exception:
        db.rollback()
        stored_path.unlink(missing_ok=True)
        raise