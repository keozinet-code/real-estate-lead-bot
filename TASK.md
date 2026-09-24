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
| Frontend features | Completed |
| Integration/deployment | Not started |

## Completed

- [x] [Completed] DOC-001–015 — Initial documentation suite
- [x] [Completed] ADR-001 — Record AI extraction boundary
- [x] [Completed] SETUP-001–006 — Application and repository foundation
- [x] [Completed] DB-001–008 — Lead, idempotency, and AI audit migrations
- [x] [Completed] API-001–008 — Lead API, idempotency, and n8n client
- [x] [Completed] QUAL-001–004 — Deterministic qualification
- [x] [Completed] N8N-001–002 — Intake and error workflow exports
- [x] [Completed] AI-001–005 — Validated, versioned AI extraction and scenarios
- [x] [Completed] UI-001 — Build responsive enquiry form
- [x] [Completed] UI-002 — Generate and reuse idempotency keys
- [x] [Completed] UI-003 — Add loading, success, duplicate, and error states
- [x] [Completed] UI-004 — Add accessibility and frontend tests
- [x] [Completed] TEST-001–002 — Health and qualification tests

## Next work

- [ ] [In Progress] DOC-016 — Final cross-contract review
- [ ] [In Progress] TEST-003–004 — Backend tests added; execution pending
- [ ] [Not Started] TEST-005 — Import and execute workflows in n8n
- [ ] [Not Started] TEST-006 — PostgreSQL migration/integration tests
- [ ] [Not Started] TEST-007 — Live-provider semantic smoke tests
- [ ] [Not Started] INT-001 — Add integration/E2E/failure tests
- [ ] [Not Started] DEPLOY-001 — Production Compose, HTTPS, backups, observability

## Next task

Build cross-component integration coverage for the full customer-to-database
path, duplicate retries, n8n failures, and representative lead scenarios.
