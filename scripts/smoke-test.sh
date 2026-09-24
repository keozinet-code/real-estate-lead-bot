#!/usr/bin/env bash
set -Eeuo pipefail

base_url="${1:-http://localhost}"
idempotency_key="smoke-$(date +%s)-${RANDOM}"

health_status="$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' "${base_url}/health")"
if [[ "${health_status}" != "200" ]]; then
  echo "Health check failed with HTTP ${health_status}" >&2
  exit 1
fi

response_file="$(mktemp)"
trap 'rm -f "${response_file}"' EXIT

lead_status="$(curl --silent --show-error --output "${response_file}" --write-out '%{http_code}' \
  --request POST "${base_url}/api/v1/leads" \
  --header 'Content-Type: application/json' \
  --header "Idempotency-Key: ${idempotency_key}" \
  --data '{"name":"Deployment Smoke Test","phone":"08000000000","message":"I want to buy a 3-bedroom apartment in Lekki within 3 months.","property_type":"apartment","location":"Lekki","bedrooms":3,"budget":80000000,"intent":"buy","timeline":"within 3 months"}')"

if [[ "${lead_status}" != "201" ]]; then
  echo "Lead smoke test failed with HTTP ${lead_status}" >&2
  cat "${response_file}" >&2
  exit 1
fi

echo "Smoke test passed: health=200 lead=201"

