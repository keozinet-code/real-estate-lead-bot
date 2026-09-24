# Project Structure and Foundation

## Ownership

| Area | Responsibility |
|---|---|
| `frontend/` | Customer UI, API client, request states, frontend tests |
| `backend/app/api/` | HTTP routes and transport boundary |
| `backend/app/schemas/` | Validated API and AI contracts |
| `backend/app/services/` | Business orchestration and deterministic qualification |
| `backend/app/repositories/` | SQLAlchemy persistence operations |
| `backend/app/integrations/` | Bounded AI and n8n clients |
| `backend/alembic/` | Versioned database migrations |
| `n8n/workflows/` | Sanitized orchestration exports |
| `infrastructure/nginx/` | HTTPS edge proxy configuration |
| `scripts/` | Deployment, smoke testing, and backup operations |
| `.github/workflows/` | Continuous verification |
| `docs/` | Product, architecture, contracts, and runbooks |

## Dependency direction

```text
React → API → service → repository → PostgreSQL
                 ↓
           AI and n8n clients
```

AI output is untrusted until validated. Deterministic qualification never runs
inside the model or n8n. React never scores or persists leads.

## Environments

- `docker-compose.yml`: local development with mounted source and Vite
- `docker-compose.prod.yml`: immutable production images, private network,
  migration gate, health checks, and HTTPS gateway
- `.env.example`: local configuration contract
- `.env.production.example`: production configuration contract

