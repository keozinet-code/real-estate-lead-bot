> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# Data Model Specification

## 1. Purpose

Define the MVP PostgreSQL data model. Exact migrations remain the source
of truth once implementation begins.

## 2. Primary Entity --- Lead

Recommended conceptual schema:

  --------------------------------------------------------------------------------
  Column              Suggested Type                Required Notes
  ------------------- ---------------- --------------------- ---------------------
  id                  UUID                               Yes Primary key

  name                VARCHAR/TEXT                        No Customer name

  email               VARCHAR/TEXT                        No Validated when
                                                             supplied

  phone               VARCHAR/TEXT                        No Preserve
                                                             international/local
                                                             format carefully

  raw_enquiry         TEXT                               Yes Original customer
                                                             enquiry

  property_type       VARCHAR/TEXT                        No apartment, house,
                                                             land, etc.

  location            VARCHAR/TEXT                        No Requested area

  bedrooms            INTEGER                             No Nullable for
                                                             land/irrelevant cases

  budget              NUMERIC                             No Normalized numeric
                                                             value where
                                                             confidently parsed

  intent              VARCHAR/ENUM                        No buy/rent/sell/land

  timeline            VARCHAR/TEXT                        No MVP may preserve
                                                             normalized text

  lead_score          INTEGER                            Yes 0--100

  lead_category       VARCHAR/ENUM                       Yes HOT/WARM/COLD

  processing_status   VARCHAR/TEXT                       Yes Processing lifecycle

  human_agent         BOOLEAN                            Yes Default false

  created_at          TIMESTAMP                          Yes Creation time

  updated_at          TIMESTAMP                          Yes Last update
  --------------------------------------------------------------------------------

## 3. Constraints

-   `lead_score` must be between 0 and 100.
-   `lead_category` must match the scoring result.
-   `bedrooms`, when supplied, must be positive.
-   `budget`, when supplied, must not be negative.
-   Intent values should be constrained to supported values where
    practical.

## 4. Indexes

Consider indexes for:

-   `created_at`
-   `lead_category`
-   `phone`
-   `email`
-   `location`
-   `processing_status`

Do not add unnecessary indexes before measuring query needs.

## 5. Duplicate Handling

A duplicate strategy should consider a request/message identifier plus
contact information and a time window. Exact idempotency behavior must
be defined in the API/workflow implementation.

## 6. Migrations

Use Alembic with FastAPI/Python.

Migration workflow:

``` text
Model change
→ Generate/review migration
→ Test locally
→ Back up production
→ Apply migration
→ Verify
```

## 7. Privacy

Lead data can contain personal information. Avoid storing unnecessary
secrets, credentials, or excessive conversational data.
