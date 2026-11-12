import pytest

from app.modules.paper_management.domain.paper import Paper


def test_create_paper():
    paper = Paper(
        id=1,
        title="  AI Research  ",
        doi=" 10.1234/ABC ",
        authors=("Ali",),
        publication_year=2025,
    )

    assert paper.title == "AI Research"
    assert paper.doi == "10.1234/abc"


def test_reject_empty_title():
    with pytest.raises(ValueError):
        Paper(id=1, title="   ")


def test_reject_invalid_year():
    with pytest.raises(ValueError):
        Paper(id=1, title="AI Research", publication_year=500)