# Project Structure and Foundation

## Ownership

| Area | Responsibility |
|---|---|
| `frontend/` | Customer UI, client validation, API calls, UI states |
| `backend/app/api/` | HTTP routes and transport boundary |
| `backend/app/schemas/` | Validated API/integration contracts |
| `backend/app/services/` | Business orchestration and integrations |
| `backend/app/repositories/` | SQLAlchemy persistence operations |
| `backend/app/models/` | Database entities |
| `n8n/workflows/` | Workflow orchestration and routing |
| `infrastructure/` | Proxy and deployment configuration |
| `tests/` | Cross-component verification |

## Backend dependency direction

```text
API → service → repository → model → PostgreSQL
          ↓
     n8n/AI clients
```

The foundation now includes PostgreSQL/Alembic, a FastAPI factory and health route, versioned API boundary, Pydantic contract scaffolding, database session dependency, React/Vite/TypeScript shell, n8n service and persistent volume, Nginx location, and a backend health test.

## Next order

1. Define “buying soon” and “clear requirements”.
2. Implement and test deterministic scoring.
3. Implement lead repository/service and `POST /api/v1/leads`.
4. Add idempotency, n8n intake, and AI output validation.
5. Build the enquiry UI and integration tests.
6. Harden production Compose/Nginx.
