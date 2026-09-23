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
- [x] [Completed] DB-001–006 — PostgreSQL model, constraints, Alembic, and verified persistence
- [x] [Completed] API-001 — Initialize FastAPI app
- [x] [Completed] API-002 — Configure settings and CORS
- [x] [Completed] API-003 — Implement `GET /health`
- [x] [Completed] QUAL-001 — Define 90-day “buying soon” rule
- [x] [Completed] QUAL-002 — Define “clear requirements”
- [x] [Completed] QUAL-003 — Implement scoring and classification
- [x] [Completed] QUAL-004 — Add category boundary and rule tests
- [x] [Completed] TEST-001 — Add health test
- [x] [Completed] TEST-002 — Add qualification tests

## Next work

- [ ] [In Progress] DOC-016 — Cross-check remaining contracts
- [ ] [Not Started] API-004 — Implement lead repository
- [ ] [Not Started] API-005 — Implement lead service
- [ ] [Not Started] API-006 — Implement `POST /api/v1/leads`
- [ ] [Not Started] API-007 — Implement idempotency
- [ ] [Not Started] API-008 — Connect n8n with timeout/error handling
- [ ] [Not Started] TEST-003 — Add lead repository/API tests
- [ ] [Not Started] N8N-001 — Implement and export intake/error workflows
- [ ] [Not Started] AI-001 — Implement validated structured extraction
- [ ] [Not Started] UI-001 — Build and test enquiry interface
- [ ] [Not Started] INT-001 — Add integration/E2E/failure tests
- [ ] [Not Started] DEPLOY-001 — Production Compose, HTTPS, backups, observability

## Next task

Implement the lead repository and service boundary before exposing `POST /api/v1/leads`.
