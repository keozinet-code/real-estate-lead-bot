# Operational Scripts

| Script | Purpose |
|---|---|
| `deploy.sh` | Validate configuration, build images, and start production services |
| `smoke-test.sh` | Verify the public health and lead-submission paths |
| `backup-postgres.sh` | Create a timestamped PostgreSQL custom-format backup and prune old backups |

Run scripts from the repository root. They contain no credentials and read
configuration from `.env.production` or explicit environment variables.

Before scheduling backups, perform and document a restore drill on a separate
database. Never test restoration against the production database.

