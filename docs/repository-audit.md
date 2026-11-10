# Repository audit — Day 1

Audit baseline: `master` at commit `64b14cb35e730797bed4245db0eec07df0146742`.

## Keep

- FastAPI application and the existing API / service / repository separation.
- SQLAlchemy 2.0, PostgreSQL, Alembic, and the initial `papers` migration.
- PyMuPDF extraction as the document parsing foundation.
- Pydantic schemas for validated API and extraction data.
- ChromaDB temporarily, until a PostgreSQL/pgvector replacement passes parity tests.

## Rewrite or retire in later implementation steps

- `app/main.py`: keep it as the application composition point; move upload orchestration into an application service/use case.
- `app/services/pdf_loader.py`: replace fixed 100-word windows with structure-aware chunks and exact text offsets.
- `app/services/vector_store.py` and `app/services/retrieval.py`: define one retrieval port and one canonical implementation before migrating storage.
- `app/services/semantic_search.py`: consolidate or retire after confirming there are no external callers; do not keep two independent retrieval paths.
- `app/models/paper.py`: separate the scholarly work (`Paper`) from its uploaded file/version (`Document`).
- `app/api/routers/papers.py`, `app/services/paper_service.py`, and `app/repositories/paper_repository.py`: retain the layering; strengthen typing, pagination, error contracts, and tests as the domain grows.

The initial Alembic migration must remain immutable. New schema changes belong in new revisions.

## Highest-impact architectural defect

There are two competing retrieval implementations: ChromaDB-backed retrieval in `vector_store.py` and an independent in-memory/NumPy embedding search in `semantic_search.py`. They do not share a canonical storage and retrieval contract. In addition, the current `POST /documents` route extracts text but does not persist the document or chunks. The system therefore has no single end-to-end ingestion/retrieval path.

## Other verified gaps

- `chunk_pages` uses fixed 100-word windows and retains only page numbers; it cannot reliably ground extracted claims to exact source spans.
- `Paper.filename` mixes scholarly-work identity with uploaded-file metadata.
- `POST /documents` extracts before checking for an empty upload and opens the PDF again to count pages.
- `app/test_ingestion.py` performs file and Chroma operations at module import time.
- `app/db/test_connection.py` is named like a pytest module and exposes a function named `test_connection`, despite being a manual connectivity script.
- The repository had no pytest configuration, no CI workflow, and no root README at this audit baseline.
- `tests/conftest.py` requires `DATABASE_URL` and assumes the separate `researchgraph_test` database has already been migrated.

## Day 1 changes

- Added `pytest.ini` so automated discovery is restricted to the `tests/` directory. Manual scripts under `app/` are no longer imported as tests.
- Added focused PDF extraction/chunking tests.
- Added a minimal test dependency file and a GitHub Actions workflow that provisions PostgreSQL, applies Alembic migrations, and runs pytest.
- No production application behavior or existing migration was changed in this audit step.

## Validation status

The GitHub connector can inspect and commit repository content but cannot execute the test suite in the developer's local environment. The first authoritative execution result will be the GitHub Actions run triggered by this branch push. Do not describe tests as passing until that run is green.
