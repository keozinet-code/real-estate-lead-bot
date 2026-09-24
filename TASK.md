# Task Tracker

Only verified work uses `[x] [Completed]`.

## Status

| Phase | Status |
|---|---|
| Documentation | In progress |
| Project foundation | Completed |
| Database | Completed |
| Backend/API | In progress |
| AI extraction | Completed |
| Lead qualification | Completed |
| n8n automation | In progress |
| Frontend features | Not started |
| Integration/deployment | Not started |

## Completed

- [x] [Completed] DOC-001–015 — Initial documentation suite
- [x] [Completed] ADR-001 — Record AI extraction boundary
- [x] [Completed] SETUP-001–006 — Application and repository foundation
- [x] [Completed] DB-001–008 — Lead, idempotency, and AI audit migrations
- [x] [Completed] API-001–008 — Lead API, idempotency, and n8n client
- [x] [Completed] QUAL-001–004 — Deterministic qualification
- [x] [Completed] N8N-001–002 — Intake and error workflow exports
- [x] [Completed] AI-001 — Add versioned extraction prompt
- [x] [Completed] AI-002 — Add strict structured-output validation
- [x] [Completed] AI-003 — Add provider adapter and safe failure behavior
- [x] [Completed] AI-004 — Merge extraction before scoring
- [x] [Completed] AI-005 — Add seven documented test scenarios
- [x] [Completed] TEST-001–002 — Health and qualification tests

## Next work

- [ ] [In Progress] DOC-016 — Final cross-contract review
- [ ] [In Progress] TEST-003–004 — Backend tests added; execution pending
- [ ] [Not Started] TEST-005 — Import and execute workflows in n8n
- [ ] [Not Started] TEST-006 — PostgreSQL migration/integration tests
- [ ] [Not Started] TEST-007 — Live-provider semantic smoke tests
- [ ] [Not Started] UI-001 — Build enquiry form
- [ ] [Not Started] UI-002 — Generate and reuse idempotency keys
- [ ] [Not Started] UI-003 — Add loading, success, duplicate, and error states
- [ ] [Not Started] UI-004 — Add accessibility and frontend tests
- [ ] [Not Started] INT-001 — Add integration/E2E/failure tests
- [ ] [Not Started] DEPLOY-001 — Production Compose, HTTPS, backups, observability

## Next task

Build the customer-facing React enquiry interface and connect it to the
lead API with stable idempotency keys and accessible request states.
