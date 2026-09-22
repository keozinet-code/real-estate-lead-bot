# Real Estate Lead Bot

Implementation-ready MVP foundation for converting property enquiries into structured, qualified leads.

## Flow

```text
Customer → React → FastAPI → n8n → AI extraction
                              → deterministic qualification
                              → PostgreSQL
                              → sales notification
                              → customer response
```

## Current status

The repository foundation, database schema, local containers, FastAPI shell, React shell, and health endpoint are scaffolded. Lead submission, scoring, AI extraction, n8n workflows, notifications, E2E tests, and production deployment remain planned.

## Structure

```text
backend/                 FastAPI, SQLAlchemy, Alembic, backend tests
frontend/                React/Vite customer application
n8n/workflows/           Sanitized workflow exports
infrastructure/nginx/    Reverse-proxy configuration
scripts/                 Repeatable operational helpers
tests/                   Cross-component and E2E tests
docs/                    Product and engineering contracts
```

See `docs/PROJECT_STRUCTURE.md` for ownership rules.

## Local start

1. Copy `.env.example` to `.env`.
2. Replace every `CHANGE_ME`.
3. Run `docker compose up --build`.
4. Check `http://localhost:8000/health`.
5. Open `http://localhost:5173` and n8n at `http://localhost:5678`.

Run migrations with `docker compose exec backend alembic upgrade head`.
Run backend tests with `docker compose exec backend pytest`.

Before editing, read `AGENTS.md`, `TASK.md`, `IMPLEMENTATION.md`, and the relevant file under `docs/`.
