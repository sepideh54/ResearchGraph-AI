# Architecture tests

Add executable dependency-boundary tests as module implementations are introduced:
- Domain packages must not import FastAPI, SQLAlchemy, Celery, Redis, or vendor SDKs.
- A bounded context must not import another context's ORM models or repositories.
- Cross-module dependencies target public application contracts or event contracts.
- No dependency cycles between bounded contexts.

Keep exceptions narrow, explicit, and documented.
