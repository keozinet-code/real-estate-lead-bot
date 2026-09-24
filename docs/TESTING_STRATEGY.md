# Testing Strategy

## Test layers

| Layer | Coverage | Command |
|---|---|---|
| Domain | Scoring thresholds and timeline rules | `pytest` |
| Service | AI merge, idempotency, persistence, failure handling | `pytest` |
| API | Validation, status codes, duplicate responses | `pytest` |
| Integration | API → service → SQLAlchemy and duplicate row guard | `pytest` |
| Frontend | API boundary, form states, retry-key stability | `npm test` |
| Contracts | Alembic, n8n JSON, production Compose | CI jobs |
| Deployment | Public health and lead submission | `scripts/smoke-test.sh` |

## Required representative cases

- Buy 3-bedroom apartment in Lekki, ₦80m, within three months
- Rent 2-bedroom in Ikeja
- Land in Ibadan below ₦20m
- Incomplete information
- Explicit HUMAN_AGENT request
- Ambiguous budget
- Duplicate submission using the same idempotency key
- AI provider failure
- n8n timeout/rejection

The AI cases use synthetic provider responses. Live-provider tests are manual
release checks because they require credentials, incur cost, and can be
nondeterministic.

## Release gate

A release requires green CI, successful migrations against a staging database,
successful n8n workflow import, a backup/restore drill, and the public smoke
test. Production credentials must never be used in automated pull-request jobs.

