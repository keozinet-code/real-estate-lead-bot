# Production Deployment Runbook

## Target

One Ubuntu VPS running Docker Compose behind Nginx:

```text
Internet → HTTPS Nginx → React static site
                       → FastAPI → PostgreSQL
                                 → n8n
```

PostgreSQL, FastAPI, the frontend container, and n8n stay on a private Docker
network. Only Nginx exposes ports 80 and 443.

## Prerequisites

- Ubuntu VPS with Docker Engine and the Compose plugin
- DNS A/AAAA record for the chosen domain
- TLS certificate and private key readable by Docker
- A pinned n8n image tag or digest
- Off-server destination for encrypted database backups

## First deployment

1. Clone the repository and check out the reviewed release commit.
2. Copy `.env.production.example` to `.env.production`.
3. Replace every `CHANGE_ME`; keep the file mode at `600`.
4. Set `TLS_CERT_PATH` and `TLS_KEY_PATH` to existing certificate files.
5. Import `n8n/workflows/99-error-handler.v1.json`, then the versioned intake
   and follow-up workflows. Configure credentials inside n8n, not in exports.
6. Activate the workflows and verify the production webhook URL/token.
7. Run `scripts/deploy.sh`.
8. Run `scripts/smoke-test.sh https://your-domain.example`.
9. Confirm one lead row and one workflow execution for the smoke-test key.

The one-shot `migrate` service applies Alembic migrations before FastAPI starts.
If migration fails, the backend remains stopped.

## Backups

Set `BACKUP_DIR` to an explicit mounted path and run
`scripts/backup-postgres.sh` from cron. Copy completed dumps off the VPS. Test a
restore on a separate database before launch and quarterly thereafter.

## Rollback

1. Stop new deployments and record the failing commit/image identifiers.
2. If the database schema is backward-compatible, check out the previous
   release and run the deployment script.
3. Never downgrade a migration without reviewing its `downgrade()` data impact.
4. For destructive schema incidents, restore into a new database first, verify
   it, then switch the application connection.

## Observability

Monitor container restarts, `/health`, HTTP 5xx rate, n8n failed executions,
PostgreSQL disk usage, backup age, and TLS expiry. Do not log raw enquiry text,
tokens, API keys, or database credentials.

