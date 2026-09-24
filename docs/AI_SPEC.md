# AI Extraction Specification

## Boundary

AI extracts facts only. FastAPI validates its output, merges it with
explicit customer fields, calculates the deterministic score, persists
the lead, and then dispatches n8n.

The provider adapter accepts any OpenAI-compatible chat-completions
endpoint. Provider configuration is external to source control.

## Prompt

- File: `backend/app/prompts/lead_extraction_v1.txt`
- Version: `lead-extraction-v1`
- Temperature: `0`
- Output: one JSON object, no prose

## Exact structured output

```json
{
  "name": null,
  "email": null,
  "phone": null,
  "property_type": null,
  "location": null,
  "bedrooms": null,
  "budget": null,
  "intent": null,
  "timeline": null,
  "human_agent": false,
  "missing_fields": [],
  "ambiguous_fields": []
}
```

Unknown values are null. Extra keys are rejected. Supported intent values
are `buy`, `rent`, `sell`, and `land`.

If a field is listed in `ambiguous_fields`, its scalar value must be
null. Duplicate missing/ambiguous entries are removed during validation.

## Merge rules

Validated fields explicitly supplied through the API always take
priority. AI may fill only fields that are absent from the request.
AI never changes the original enquiry or idempotency key.

## Failure rules

Timeout, provider rejection, invalid JSON, extra keys, wrong types, or
contradictory ambiguity produce a safe outcome:

- preserve and store the original enquiry
- do not fabricate extracted values
- set `human_agent=true`
- persist the prompt version and empty validated extraction
- continue deterministic scoring only with confirmed explicit fields
- route n8n to `HUMAN_AGENT`

Secrets and raw provider error bodies must not be returned to customers.

## Required test scenarios

1. Buy: 3-bedroom apartment, Lekki, ₦80m, within 3 months
2. Rent: 2-bedroom apartment, Ikeja
3. Land: Ibadan, below ₦20m
4. Incomplete enquiry: unknown fields remain null and are reported
5. HUMAN_AGENT: explicit request sets escalation
6. Ambiguous budget: budget remains null and is reported
7. Duplicate request: the AI provider is called once for one
   idempotency key

The tests use a fake provider. Live-provider semantic evaluation remains
a separate smoke test because model output is probabilistic.
