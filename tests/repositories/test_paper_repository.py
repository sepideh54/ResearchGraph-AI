from app.repositories import paper_repository


def test_create_paper(db_session):
    paper_data = {
        "title": "Test Research Paper",
        "filename": "test-paper.pdf"
    }

    paper = paper_repository.create_paper(
        db_session,
        paper_data
    )

    assert paper.id is not None
    assert paper.title == "Test Research Paper"
    assert paper.filename == "test-paper.pdf"


def test_get_paper(db_session):
    paper = paper_repository.create_paper(
        db_session,
        {
            "title": "Test Paper",
            "filename": "test.pdf"
        }
    )

    retrieved_paper = db_session.get(
        paper.__class__,
        paper.id
    )

    assert retrieved_paper is not None
    assert retrieved_paper.id == paper.id
    assert retrieved_paper.title == "Test Paper"


def test_delete_paper(db_session):
    paper = paper_repository.create_paper(
        db_session,
        {
            "title": "Delete Test",
            "filename": "delete.pdf"
        }
    )

    paper_repository.delete_paper(db_session, paper.id)

    db_session.flush()

    deleted_paper = db_session.get(
        paper.__class__,
        paper.id
    )

    assert deleted_paper is None    

def test_update_paper(db_session):
    paper = paper_repository.create_paper(
        db_session,
        {
            "title": "Original Title",
            "filename": "test.pdf"
        }
    )

    updated_paper = paper_repository.update_paper(
        db_session,
        paper.id,
        {"title": "Updated Title"}
    )

    assert updated_paper is not None
    assert updated_paper.id == paper.id
    assert updated_paper.title == "Updated Title"


def test_get_nonexistent_paper(db_session):
    paper = paper_repository.get_paper(db_session, 999999)

    assert paper is None


def test_update_nonexistent_paper(db_session):
    updated_paper = paper_repository.update_paper(
        db_session,
        999999,
        {"title": "Updated Title"}
    )

    assert updated_paper is None


def test_delete_nonexistent_paper(db_session):
    result = paper_repository.delete_paper(
        db_session,
        999999
    )

    assert result is None                