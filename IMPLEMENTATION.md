# Engineering Progress Log

`TASK.md` tracks planned work; this file records verified implementation.

## Snapshot

- Overall: In progress
- Current phase: AI extraction
- Production: Not started
- Next: AI-001 through AI-003

## 2026-09-24 — FastAPI to n8n integration

Implemented on `chore/repository-scaffolding`:

- Allow-listed Pydantic workflow payload
- Authenticated `X-Webhook-Token` delivery
- Configurable timeout constrained to 1–30 seconds
- Safe timeout, network, 4xx, 5xx, and invalid-response handling
- No hidden automatic HTTP retry
- `workflow_pending`, `workflow_dispatched`, and
  `workflow_failed` processing states
- Same-key retry only for failed workflow dispatch
- n8n client tests using an in-memory HTTP transport
- Sanitized `01-lead-intake.v1.json` workflow
- Sanitized `99-error-handler.v1.json` workflow
- Header Auth credential setup documentation
- Defensive n8n duplicate check and bounded static-data retention
- Synchronized API/workflow specifications and environment template

Verification:

- Python syntax compilation: PASS
- Workflow JSON parsing: PASS
- Static workflow connection/node-reference validation: PASS
- Source-level payload/secret review: PASS
- Full pytest suite: NOT RUN because project dependencies are not
  installed in this execution environment
- n8n import/execution: NOT RUN; requires a running configured instance

## 2026-09-24 — Lead repository, API, and idempotency

Implemented repository/service/API boundaries, required idempotency,
backward-compatible migration, race recovery, and tests. Syntax and
contracts passed; PostgreSQL integration remains pending.

## 2026-09-23 — Deterministic lead qualification

Implemented shared domain types, exact rules, scoring, categories, audit
output, and tests. Local qualification smoke test: PASS.

## Components

| Component | Status |
|---|---|
| PostgreSQL/Alembic | Schema and migrations implemented; live verification pending |
| Lead API/idempotency | Implemented; full tests pending |
| Qualification | Implemented and smoke-tested |
| FastAPI-to-n8n client | Implemented and syntax-verified |
| n8n intake/error exports | Implemented and JSON-verified |
| AI extraction | Not started |
| React shell | Scaffolded |
| Enquiry UI | Not started |
| Production deployment | Not started |
