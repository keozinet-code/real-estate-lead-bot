# Real Estate Lead Bot

A production-packaged MVP that converts property enquiries into structured,
qualified, deduplicated leads and dispatches them to automated follow-up.

## Flow

```text
Customer → React → FastAPI → validated AI extraction
                          → deterministic qualification
                          → PostgreSQL
                          → n8n → sales/customer follow-up
```

## Capabilities

- Responsive and accessible customer enquiry interface
- Typed, validated lead API with stable idempotency keys
- Strict versioned AI extraction with ambiguity and HUMAN_AGENT safeguards
- Deterministic HOT/WARM/COLD scoring
- PostgreSQL persistence and Alembic migrations
- Authenticated, allow-listed n8n dispatch
- Versioned intake, follow-up, and error workflows
- Automated frontend, backend, integration, and contract checks
- Production Docker images, HTTPS Nginx, backups, and deployment runbook

## Repository

```text
backend/                 FastAPI, SQLAlchemy, Alembic, tests
frontend/                React/Vite customer application and tests
n8n/workflows/           Sanitized workflow exports
infrastructure/nginx/    Development and production proxy configuration
scripts/                 Deployment, smoke test, and backup helpers
docs/                    Product, engineering, testing, and operations contracts
.github/workflows/       CI release gates
```

See `docs/PROJECT_STRUCTURE.md` for ownership boundaries.

## Local development

1. Copy `.env.example` to `.env` and replace every `CHANGE_ME`.
2. Run `docker compose up --build`.
3. Run migrations: `docker compose exec backend alembic upgrade head`.
4. Open `http://localhost:5173`; health is at `http://localhost:8000/health`.

Tests:

```bash
docker compose exec backend pytest
docker compose exec frontend npm test
```

## Production

Production is intentionally a separate configuration:

```bash
cp .env.production.example .env.production
# replace placeholders and configure DNS/TLS/n8n
scripts/deploy.sh
scripts/smoke-test.sh https://your-domain.example
```

Read `docs/DEPLOYMENT.md` before launch. Do not commit `.env.production`, TLS
private keys, workflow credentials, or database dumps.

