# Engineering Progress Log

`TASK.md` tracks planned work; this file records verified implementation.

## Snapshot

- Overall: In progress
- Current phase: Frontend enquiry experience
- Production: Not started
- Next: UI-001 through UI-004

## 2026-09-24 — Validated AI extraction

Implemented on `chore/repository-scaffolding`:

- Versioned `lead-extraction-v1` prompt
- Provider-neutral protocol and OpenAI-compatible HTTP adapter
- Strict Pydantic output schema with extra-field rejection
- Missing/ambiguous field tracking and ambiguity invariants
- Explicit-field-over-AI merge before qualification
- Safe provider/validation failure route to HUMAN_AGENT
- Prompt version, missing fields, and ambiguous fields persisted
- Backward-compatible AI audit Alembic migration
- AI audit fields forwarded through the allow-listed n8n payload
- Six semantic extraction scenarios plus duplicate provider-call guard
- ADR-001 documenting the corrected AI trust boundary
- Updated architecture, AI specification, task tracker, and environment
  configuration

Verification:

- Python syntax compilation: PASS
- Prompt/package resource inspection: PASS
- Workflow JSON parsing: PASS
- Seven scenario contract coverage: source-inspected
- Full pytest suite: NOT RUN because dependencies are unavailable
- Live AI provider test: NOT RUN; requires configured credentials

## 2026-09-24 — FastAPI to n8n integration

Implemented authenticated bounded workflow dispatch, safe failures,
workflow states, n8n tests, and sanitized intake/error exports. Python
and workflow JSON validation passed.

## 2026-09-24 — Lead API and idempotency

Implemented repository/service/API boundaries, database idempotency,
race recovery, and tests.

## Components

| Component | Status |
|---|---|
| Database migrations | Implemented; live verification pending |
| Lead API/idempotency | Implemented; full tests pending |
| Qualification | Implemented and smoke-tested |
| AI extraction | Implemented and syntax-verified |
| FastAPI-to-n8n | Implemented and syntax-verified |
| n8n exports | JSON-verified; live import pending |
| React shell | Scaffolded |
| Enquiry UI | Not started |
| Production deployment | Not started |
