# System Architecture

## Runtime flow

```text
Customer
→ React
→ FastAPI request validation and idempotency lookup
→ AI extraction adapter
→ Pydantic structured-output validation
→ Explicit-field merge
→ Deterministic qualification
→ PostgreSQL
→ Authenticated n8n workflow
→ Sales routing, notifications, and follow-up
```

Production remains one existing VPS behind Nginx using Docker Compose
for React, FastAPI, PostgreSQL, and n8n.

## Responsibilities

| Component | Responsibility |
|---|---|
| React | Customer form/chat, client validation, UI states |
| FastAPI | Public API, AI trust boundary, deterministic scoring, persistence, idempotency, n8n invocation |
| AI provider | Structured extraction only; no scores or side effects |
| PostgreSQL | Durable lead, extraction audit, state, and idempotency |
| n8n | Routing, notifications, CRM actions, follow-up, workflow errors |
| Nginx | HTTPS and reverse proxy |

## Design rules

- AI output is untrusted until Pydantic validation succeeds.
- Explicit customer fields override extracted fields.
- Deterministic business rules have one implementation.
- n8n never stores source-controlled credentials.
- Duplicate requests must not repeat AI or workflow side effects.
- Raw enquiries are preserved for recovery and human review.

See `docs/adr/ADR-001-ai-extraction-boundary.md` for the recorded
architecture revision.
