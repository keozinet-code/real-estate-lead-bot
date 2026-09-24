# Workflow Specification

## FastAPI to n8n contract

FastAPI sends only allow-listed lead fields to:

```text
POST /webhook/lead-intake-v1
X-Webhook-Token: <secret>
Idempotency-Key: <same key used by the lead API>
```

Connection and total request time are bounded by
`N8N_TIMEOUT_SECONDS` (default five seconds). The client performs no
automatic retries. The caller retries the lead API using the same
idempotency key.

Expected n8n response:

```json
{
  "accepted": true,
  "duplicate": false,
  "workflow": "lead-intake-v1"
}
```

## Current intake workflow

```text
Authenticated Webhook
→ Validate and allow-list fields
→ Defensive duplicate check
→ Existing key ───────────────→ Respond duplicate
→ New key
→ Prepare HOT/WARM/COLD/HUMAN_AGENT route
→ Mark processed
→ Respond accepted
```

FastAPI/PostgreSQL remains the authoritative idempotency layer. n8n's
static-data check is defense in depth and must not replace the database
unique constraint.

## Processing states

- `workflow_pending`: saved and eligible for dispatch
- `workflow_dispatched`: n8n accepted the lead
- `workflow_failed`: dispatch failed safely and may be retried using
  the same idempotency key

A duplicate request normally returns the existing lead without another
workflow call. A duplicate whose existing state is `workflow_failed`
is allowed to retry dispatch.

## Failure behavior

- Network timeout, connection failure, or n8n 5xx: save
  `workflow_failed`, return a safe `503`, and disclose no internal
  response body.
- n8n 4xx or invalid response: treat as rejected, save
  `workflow_failed`, and return a safe `503`.
- Workflow runtime failure: route to the imported error workflow, which
  keeps only workflow/execution identifiers and a truncated message.

## Credential setup

The workflow export contains no credentials. After import, configure an
n8n Header Auth credential named for the FastAPI webhook using:

- Header: `X-Webhook-Token`
- Value: the same secret as `N8N_WEBHOOK_TOKEN`

Store that credential encrypted in n8n. Never add it to workflow JSON,
logs, documentation, or Git.

## Future nodes

AI extraction, sales notifications, CRM updates, and customer follow-up
remain intentionally unimplemented. They will attach after the
`Prepare Route` node and must preserve the same idempotency contract.
