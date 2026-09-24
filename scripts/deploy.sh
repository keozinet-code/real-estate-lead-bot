#!/usr/bin/env bash
set -Eeuo pipefail

compose_file="${COMPOSE_FILE:-docker-compose.prod.yml}"
env_file="${ENV_FILE:-.env.production}"

test -f "${env_file}" || { echo "Missing ${env_file}" >&2; exit 1; }
grep -q 'CHANGE_ME' "${env_file}" && { echo "Replace every CHANGE_ME value before deployment" >&2; exit 1; }

docker compose --env-file "${env_file}" -f "${compose_file}" config --quiet
docker compose --env-file "${env_file}" -f "${compose_file}" build --pull
docker compose --env-file "${env_file}" -f "${compose_file}" up -d --remove-orphans
docker compose --env-file "${env_file}" -f "${compose_file}" ps

