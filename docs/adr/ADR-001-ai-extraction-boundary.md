# ADR-001: Validate AI extraction in FastAPI

## Status

Accepted — 2026-09-24

## Context

The original architecture assigned AI processing and deterministic
qualification to n8n. The implemented system now has explicit Pydantic
contracts, deterministic scoring, persistence, idempotency, and failure
handling in FastAPI. Letting unvalidated n8n/LLM output write directly to
the database would create two competing business-rule authorities.

## Decision

FastAPI owns the AI extraction trust boundary:

```text
Customer → FastAPI validation → AI extraction adapter
         → Pydantic output validation
         → explicit-field merge
         → deterministic qualification
         → PostgreSQL
         → n8n orchestration
```

n8n remains responsible for workflow routing, notifications, CRM
actions, follow-up, and error automation. The AI provider uses a
replaceable interface; the first adapter supports an OpenAI-compatible
chat-completions endpoint.

## Consequences

- AI output cannot bypass validation or assign scores.
- Explicit form fields override AI-extracted values.
- Provider failures preserve the raw enquiry and route to HUMAN_AGENT.
- Prompt version, missing fields, and ambiguous fields are persisted.
- Changing AI vendors does not change the service or scoring contracts.
- The architecture documentation and n8n workflow must reflect that AI
  extraction happens before workflow dispatch.
