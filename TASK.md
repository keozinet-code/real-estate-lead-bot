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
| Lead qualification | Not started |
| n8n automation | Not started |
| Frontend features | Not started |
| Integration/deployment | Not started |

## Completed

- [x] [Completed] DOC-001–015 — Initial documentation suite
- [x] [Completed] SETUP-001 — Organize repository structure
- [x] [Completed] SETUP-002 — Create safe environment template
- [x] [Completed] SETUP-003 — Configure local Compose foundation
- [x] [Completed] SETUP-004 — Scaffold FastAPI
- [x] [Completed] SETUP-005 — Scaffold React/Vite
- [x] [Completed] SETUP-006 — Establish n8n, infrastructure, and test boundaries
- [x] [Completed] DB-001–006 — PostgreSQL model, constraints, Alembic, and verified persistence
- [x] [Completed] API-001 — Initialize FastAPI app
- [x] [Completed] API-002 — Configure settings and CORS
- [x] [Completed] API-003 — Implement `GET /health`
- [x] [Completed] TEST-001 — Add health test

## Next work

- [ ] [In Progress] DOC-016 — Cross-check contracts against scaffold
- [ ] [Not Started] QUAL-001 — Define deterministic “buying soon”
- [ ] [Not Started] QUAL-002 — Define deterministic “clear requirements”
- [ ] [Not Started] QUAL-003 — Implement and test scoring/classification
- [ ] [Not Started] API-004 — Implement lead repository/service
- [ ] [Not Started] API-005 — Implement `POST /api/v1/leads`
- [ ] [Not Started] API-006 — Implement idempotency
- [ ] [Not Started] API-007 — Connect n8n with timeout/error handling
- [ ] [Not Started] N8N-001 — Implement and export intake/error workflows
- [ ] [Not Started] AI-001 — Implement validated structured extraction
- [ ] [Not Started] UI-001 — Build and test enquiry interface
- [ ] [Not Started] INT-001 — Add integration/E2E/failure tests
- [ ] [Not Started] DEPLOY-001 — Production Compose, HTTPS, backups, observability

## Next task

Complete QUAL-001 and QUAL-002 before implementing scoring.
