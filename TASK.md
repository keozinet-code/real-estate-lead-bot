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
| n8n automation | Not started |
| Frontend features | Not started |
| Integration/deployment | Not started |

## Completed

- [x] [Completed] DOC-001–015 — Initial documentation suite
- [x] [Completed] SETUP-001–006 — Application and repository foundation
- [x] [Completed] DB-001–006 — Initial PostgreSQL model and migration
- [x] [Completed] DB-007 — Add idempotency-key migration
- [x] [Completed] API-001–003 — FastAPI foundation and health endpoint
- [x] [Completed] API-004 — Implement lead repository
- [x] [Completed] API-005 — Implement lead service
- [x] [Completed] API-006 — Implement `POST /api/v1/leads`
- [x] [Completed] API-007 — Implement idempotency
- [x] [Completed] QUAL-001–004 — Deterministic qualification and tests
- [x] [Completed] TEST-001–002 — Health and qualification tests

## Next work

- [ ] [In Progress] DOC-016 — Cross-check remaining contracts
- [ ] [In Progress] TEST-003 — Service/API tests added; full execution pending
- [ ] [Not Started] API-008 — Connect n8n with bounded timeout/error handling
- [ ] [Not Started] TEST-004 — Add PostgreSQL repository integration tests
- [ ] [Not Started] N8N-001 — Implement authenticated intake webhook
- [ ] [Not Started] N8N-002 — Add validation, error workflow, and duplicate guard
- [ ] [Not Started] AI-001 — Implement validated structured extraction
- [ ] [Not Started] UI-001 — Build and test enquiry interface
- [ ] [Not Started] INT-001 — Add integration/E2E/failure tests
- [ ] [Not Started] DEPLOY-001 — Production Compose, HTTPS, backups, observability

## Next task

Implement the bounded FastAPI-to-n8n client and the first sanitized n8n
lead-intake workflow contract.
