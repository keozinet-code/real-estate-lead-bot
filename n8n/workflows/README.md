# n8n workflows

## Included exports

- `01-lead-intake.v1.json` — authenticated intake, allow-list
  sanitization, defensive duplicate check, route preparation, and response
- `99-error-handler.v1.json` — sanitized workflow-error capture

## Import and credential setup

1. Import both JSON files into n8n.
2. Create an n8n **Header Auth** credential:
   - Header name: `X-Webhook-Token`
   - Header value: the same secret as backend `N8N_WEBHOOK_TOKEN`
3. Assign that credential to **Authenticated Lead Webhook**.
4. In the lead workflow settings, select **PrimeHomes - Error Handler v1**
   as the error workflow.
5. Activate the error workflow, then activate the lead workflow.
6. Use the production webhook URL ending in
   `/webhook/lead-intake-v1`, not the test URL.

No credentials or secret values are stored in these exports.

The n8n static-data duplicate guard is defense in depth only. PostgreSQL's
unique idempotency key in FastAPI remains the authoritative duplicate
protection.

The current intake workflow prepares `HOT`, `WARM`, `COLD`, or
`HUMAN_AGENT` routing but intentionally has no email/CRM side effects
yet. Those will be added with notification credentials in a later stage.
