# Task Tracker

Only verified work uses `[x] [Completed]`.

## Status

| Phase | Status |
|---|---|
| Documentation | In progress |
| Project foundation | Completed |
| Database | Completed |
| Backend/API | In progress |
| AI extraction | Not started |
| Lead qualification | Completed |
| n8n automation | In progress |
| Frontend features | Not started |
| Integration/deployment | Not started |

## Completed

- [x] [Completed] DOC-001–015 — Initial documentation suite
- [x] [Completed] SETUP-001–006 — Application and repository foundation
- [x] [Completed] DB-001–007 — Lead schema and idempotency migration
- [x] [Completed] API-001–007 — Health, lead API, and idempotency
- [x] [Completed] API-008 — Add bounded authenticated n8n client
- [x] [Completed] QUAL-001–004 — Deterministic qualification and tests
- [x] [Completed] N8N-001 — Add sanitized intake workflow export
- [x] [Completed] N8N-002 — Add duplicate guard and error workflow export
- [x] [Completed] TEST-001–002 — Health and qualification tests

## Next work

- [ ] [In Progress] DOC-016 — Cross-check remaining contracts
- [ ] [In Progress] TEST-003 — Service/API tests added; execution pending
- [ ] [In Progress] TEST-004 — n8n client tests added; execution pending
- [ ] [Not Started] TEST-005 — Import and execute workflows in n8n
- [ ] [Not Started] TEST-006 — PostgreSQL repository integration tests
- [ ] [Not Started] AI-001 — Define versioned AI prompt
- [ ] [Not Started] AI-002 — Validate structured AI extraction
- [ ] [Not Started] AI-003 — Add documented AI test cases
- [ ] [Not Started] N8N-003 — Attach AI extraction to intake workflow
- [ ] [Not Started] UI-001 — Build and test enquiry interface
- [ ] [Not Started] INT-001 — Add integration/E2E/failure tests
- [ ] [Not Started] DEPLOY-001 — Production Compose, HTTPS, backups, observability

## Next task

Implement validated AI extraction with a versioned prompt and the seven
documented test scenarios, then attach it before deterministic scoring.
