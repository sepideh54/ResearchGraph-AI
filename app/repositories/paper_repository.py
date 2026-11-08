from sqlalchemy.orm import Session
from app.models.paper import Paper
from sqlalchemy import select

def create_paper(db: Session, paper_data: dict):
    paper = Paper(**paper_data)

    db.add(paper)
    db.flush()

    return paper


def get_paper(db: Session, paper_id: int):
    result = db.execute(
        select(Paper).where(Paper.id == paper_id)
    )

    paper = result.scalar_one_or_none()

    return paper


def get_all_papers(db: Session):
    result = db.execute(select(Paper))
    papers = result.scalars().all()

    return papers

def update_paper(db: Session, paper_id: int, update_data: dict):
    paper = get_paper(db, paper_id)

    if paper is None:
        return None

    allowed_fields = {"title"}

    for key, value in update_data.items():
        if key not in allowed_fields:
            raise ValueError(f"Field '{key}' cannot be updated")

        setattr(paper, key, value)
    db.flush()

    return paper



def delete_paper(db: Session, paper_id: int):
    paper = get_paper(db, paper_id)

    if paper is None:
        return None

    db.delete(paper)
    db.flush()

    return paper
