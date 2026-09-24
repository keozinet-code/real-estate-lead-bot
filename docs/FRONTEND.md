# Frontend Enquiry Experience

## Responsibility

The React application collects customer input and presents request states. It
does not score leads or infer missing details; those remain backend concerns.

## Structure

| Path | Responsibility |
|---|---|
| `src/api/leads.ts` | HTTP boundary, idempotency-key generation, safe errors |
| `src/types/lead.ts` | Request and response contracts |
| `src/components/LeadForm.tsx` | Controlled form and submission lifecycle |
| `src/components/SubmissionResult.tsx` | Success and duplicate presentation |
| `src/styles.css` | Responsive visual system and accessible interaction states |

## Idempotency lifecycle

1. Generate a key when the form instance starts.
2. Reuse that key for every retry of the same entered enquiry.
3. Preserve all fields when a request fails.
4. Generate a new key only after a successful response.
5. Starting another enquiry mounts a fresh form and fresh key.

## Configuration

`VITE_API_BASE_URL` is optional. When omitted, requests use the same origin,
which is appropriate behind Nginx. Local Compose supplies
`http://localhost:8000`.

## Commands

```bash
npm install
npm run build
npm test
```

The live browser/API path is covered by the next integration stage.
