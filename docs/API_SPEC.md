# API Specification

## Health

### `GET /health`

Returns `200 {"status": "ok"}`.

## Submit lead

### `POST /api/v1/leads`

Every request must include:

```text
Idempotency-Key: <8-128 safe characters>
```

Allowed key characters are letters, numbers, dots, underscores, colons,
and hyphens. The frontend should generate one UUID per user submission
and reuse it when retrying that same submission.

Example request:

```json
{
  "name": "Amina Yusuf",
  "email": "amina@example.com",
  "phone": "08000000000",
  "message": "I want to buy a 3-bedroom apartment in Lekki.",
  "property_type": "apartment",
  "location": "Lekki",
  "bedrooms": 3,
  "budget": 80000000,
  "intent": "buy",
  "timeline": "within 3 months"
}
```

Only `message` is required in the JSON body. Structured fields are
optional because later AI processing may extract them from the message.

New submission response: `201 Created`.

```json
{
  "success": true,
  "lead_id": "uuid",
  "status": "qualified",
  "message": "Your enquiry has been received.",
  "lead_score": 100,
  "lead_category": "HOT",
  "duplicate": false
}
```

Retrying the same key returns the original lead with `200 OK` and
`"duplicate": true`. It must not create another row or trigger future
duplicate workflow side effects.

## Validation

- Missing or invalid idempotency key: `422`
- Malformed JSON or invalid fields: `422`
- Empty or oversized message: `422`
- Unexpected server failure: `500`
- Dependency unavailable: `502` or `503`

Error responses must not expose stack traces, credentials, keys, or
internal secrets.

## n8n integration

FastAPI will call the configured production n8n webhook using an
environment variable. Timeout, authentication, payload, response, retry,
and failure behavior remain part of the next integration phase.

## CORS

Production must allow only approved frontend origins.
