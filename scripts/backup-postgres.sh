#!/usr/bin/env bash
set -Eeuo pipefail

compose_file="${COMPOSE_FILE:-docker-compose.prod.yml}"
env_file="${ENV_FILE:-.env.production}"
backup_dir="${BACKUP_DIR:?Set BACKUP_DIR to an explicit backup directory}"
retention_days="${BACKUP_RETENTION_DAYS:-14}"

mkdir -p "${backup_dir}"
backup_file="${backup_dir}/primehomes-$(date -u +%Y%m%dT%H%M%SZ).dump"

docker compose --env-file "${env_file}" -f "${compose_file}" exec -T postgres \
  sh -c 'pg_dump --format=custom --no-owner --username "$POSTGRES_USER" "$POSTGRES_DB"' > "${backup_file}"

test -s "${backup_file}"
find "${backup_dir}" -maxdepth 1 -type f -name 'primehomes-*.dump' -mtime "+${retention_days}" -delete
echo "Backup created: ${backup_file}"
