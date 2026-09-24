# Data Model Specification

## Lead

| Column | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| idempotency_key | VARCHAR(128) | New requests | Unique request identifier; legacy rows may be null |
| name | VARCHAR(255) | No | Customer name |
| email | VARCHAR(320) | No | Validated when supplied |
| phone | VARCHAR(50) | No | Preserve customer format |
| raw_enquiry | TEXT | Yes | Original message |
| property_type | VARCHAR(100) | No | Apartment, house, land, etc. |
| location | VARCHAR(255) | No | Requested area |
| bedrooms | INTEGER | No | Positive when supplied |
| budget | NUMERIC(15,2) | No | Non-negative normalized value |
| intent | ENUM | No | buy/rent/sell/land |
| timeline | VARCHAR(100) | No | Normalized text |
| lead_score | INTEGER | Yes | 0-100 |
| lead_category | ENUM | Yes | HOT/WARM/COLD |
| processing_status | VARCHAR(50) | Yes | Processing lifecycle |
| human_agent | BOOLEAN | Yes | Defaults false |
| created_at | TIMESTAMPTZ | Yes | Creation time |
| updated_at | TIMESTAMPTZ | Yes | Last update |

## Duplicate handling

New API submissions require an `Idempotency-Key`. The
`idempotency_key` column has a unique index. A repeated key returns the
original lead. The column remains nullable so the migration is safe for
records created before idempotency support.

The unique database index is the final protection against concurrent
requests. Service code catches a unique-key race, rolls back, retrieves
the original lead, and returns it as a duplicate.

## Constraints and indexes

- Score must be between 0 and 100.
- Bedrooms must be positive when supplied.
- Budget must be non-negative when supplied.
- Supported intent values are constrained by an enum.
- Indexed fields include idempotency key, timestamps, category, contact
  fields, location, and processing status.

Exact Alembic migrations are the source of truth.
