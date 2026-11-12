from sqlalchemy.orm import Session
from app.repositories import paper_repository

def create_paper(db: Session, paper_data: dict):
    try:
        paper = paper_repository.create_paper(db, paper_data)
        db.commit()
        db.refresh(paper)
        return paper
    except Exception:
        db.rollback()
        raise

def get_paper(db: Session, paper_id: int):
    return paper_repository.get_paper(db, paper_id)


def get_all_papers(db: Session):
    return paper_repository.get_all_papers(db)


def update_paper(db: Session, paper_id: int, update_data: dict):
    try:
        paper = paper_repository.update_paper(db, paper_id, update_data)

        if paper is None:
            return None

        db.commit()
        db.refresh(paper)
        return paper
    except Exception:
        db.rollback()
        raise


def delete_paper(db: Session, paper_id: int):
    try:
        paper = paper_repository.delete_paper(db, paper_id)

        if paper is None:
            return None

        db.commit()
        return paper
    except Exception:
        db.rollback()
        raise