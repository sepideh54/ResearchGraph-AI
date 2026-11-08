# Bounded-context package map

| Module | Ownership |
|---|---|
| paper_management | Scientific-work identity and bibliographic metadata; not PDF binaries. |
| document_processing | Document versions, PDF lifecycle, extraction, and storage port. |
| knowledge_processing | Chunks, embeddings, model-version metadata, vector-index lifecycle. |
| knowledge_retrieval | Semantic/hybrid retrieval, filtering, reranking, retrieval policy. |
| research_intelligence | Multi-stage RAG orchestration, evidence assembly, answers, and citations. |
| knowledge_graph | Concepts, entities, relationships, graph queries. |
| ai_agent | Agent orchestration, adaptive questions, controlled tool invocation. MCP is a protocol adapter, not the agent domain. |
| identity_access | Users, roles, permissions, authentication and authorization. |
| workflow | Durable job lifecycle, attempts, retry scheduling, leases, workflow coordination. Celery and Redis are adapters/infrastructure. |

## Target layers inside each module

Create these packages when the first real implementation is migrated:
- `domain/`: framework-independent entities, value objects, invariants, domain events.
- `application/use_cases/`: orchestration and application services.
- `application/ports/`: repository, storage, publisher, and other required interfaces.
- `application/contracts/`: public DTOs and cross-module contracts.
- `adapters/inbound/`: HTTP, worker, CLI, or MCP entry points.
- `adapters/outbound/`: persistence, broker, storage, and provider implementations.
- `infrastructure/`: module-specific technical configuration when needed.

## Dependency rules

1. Each module owns its domain model, persistence mapping, and tables.
2. Other modules must not import its ORM models or repositories.
3. Cross-module interaction uses public application contracts and versioned events; identifiers cross boundaries as IDs, not ORM object references.
4. Domain packages must not import FastAPI, SQLAlchemy, Celery, Redis, filesystem APIs, or vendor SDKs.
5. Inbound adapters translate external requests into use-case calls. Outbound adapters implement ports defined inward.
6. Use in-process contracts for immediate calls and durable events for state-change notifications.
7. Keep shared code small and stable; do not move business rules into a catch-all shared package.

## Legacy migration policy

Existing `app/api`, `app/services`, `app/repositories`, `app/models`, and `app/db` packages are retained temporarily. They are legacy implementation, not assumed to satisfy the new boundaries. Migrate one vertical slice at a time behind tests; do not delete or rename persisted data as part of a folder-only refactor.
