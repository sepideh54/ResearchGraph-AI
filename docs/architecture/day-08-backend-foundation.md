# Day 8 — Backend foundation and module boundaries

## Completed in this change

- Added the top-level `bootstrap`, `modules`, and `shared` package boundaries.
- Added Python package roots for all nine approved bounded contexts.
- Documented module ownership, target internal layers, allowed dependency direction, and legacy migration policy.
- Preserved existing API routes, Paper CRUD behavior, PDF extraction code, ChromaDB retrieval, database session, and Alembic history. No existing route, table, or stored record was intentionally removed.

## Target package layout

```text
app/
├── bootstrap/
├── modules/
│   ├── paper_management/
│   ├── document_processing/
│   ├── knowledge_processing/
│   ├── knowledge_retrieval/
│   ├── research_intelligence/
│   ├── knowledge_graph/
│   ├── ai_agent/
│   ├── identity_access/
│   └── workflow/
└── shared/
    ├── domain/
    ├── application/
    └── infrastructure/
```

Each module will grow `domain`, `application/use_cases`, `application/ports`, `application/contracts`, `adapters/inbound`, `adapters/outbound`, and (only when needed) `infrastructure` packages as real code is migrated. Empty placeholder trees are deliberately avoided.

## Non-goals

This is a safe structural foundation, not a claim that legacy code has already been migrated to Hexagonal Architecture. No ORM model, database table, endpoint, or stored record is renamed or deleted in this change. The legacy code remains until each vertical slice is migrated and verified.

## Next implementation slice

1. Define framework-independent Paper and Document domain models and invariants.
2. Define repository and Unit of Work ports in the application layer.
3. Add SQLAlchemy persistence adapters and explicit domain/ORM mapping.
4. Add a forward-only Alembic migration to introduce Document storage without dropping legacy `papers.filename`.
5. Add data reconciliation checks; missing original PDF files must be marked for re-upload, not represented by invented paths.
6. Move Paper API routes behind inbound adapters and verify compatibility.

## Verification status

This change creates packages and architecture documentation only. Runtime imports, Alembic migration execution, pytest, and PostgreSQL integration have not been run in the local development environment and must pass before merge.
