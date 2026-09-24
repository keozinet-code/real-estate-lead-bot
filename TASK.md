# Task Tracker

Development implementation is complete. Environment-dependent release checks
remain required before production launch.

## Development status

| Phase | Status |
|---|---|
| Documentation and architecture | Completed |
| Project foundation | Completed |
| Database and migrations | Completed |
| Backend/API and idempotency | Completed |
| AI extraction | Completed |
| Lead qualification | Completed |
| n8n automation exports | Completed |
| Frontend experience | Completed |
| Integration test implementation | Completed |
| CI and production packaging | Completed |

## Completed task groups

- [x] [Completed] DOC-001–016 — Documentation and cross-contract review
- [x] [Completed] SETUP-001–006 — Repository and application foundation
- [x] [Completed] DB-001–008 — Lead, idempotency, and AI audit migrations
- [x] [Completed] API-001–008 — Lead API, persistence, and n8n dispatch
- [x] [Completed] QUAL-001–004 — Deterministic qualification
- [x] [Completed] AI-001–005 — Validated versioned AI extraction
- [x] [Completed] N8N-001–004 — Intake, follow-up, error, and payload contracts
- [x] [Completed] UI-001–004 — Responsive accessible enquiry experience
- [x] [Completed] TEST-001–007 — Automated test cases and release test plan
- [x] [Completed] INT-001 — API/persistence/idempotency integration test
- [x] [Completed] DEPLOY-001 — Production images, Compose, HTTPS proxy, CI, scripts, and runbook

## Production release checklist

These are operations, not unfinished application development:

- [ ] [Environment Required] Provision VPS, DNS, TLS, and production secrets
- [ ] [Environment Required] Import and activate n8n workflows
- [ ] [Environment Required] Run migrations against staging/production PostgreSQL
- [ ] [Environment Required] Execute live AI-provider semantic smoke tests
- [ ] [Environment Required] Perform backup and restore drill
- [ ] [Environment Required] Run public HTTPS smoke test

## Next action

Review and merge the draft PR after CI is green, then follow
`docs/DEPLOYMENT.md` on the authorized VPS.

