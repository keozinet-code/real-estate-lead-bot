> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# Testing Specification

## 1. Purpose

Define a practical MVP testing strategy covering backend/API,
PostgreSQL, AI extraction, qualification, n8n, frontend, integration,
deployment, and regression.

## 2. Testing Philosophy

-   Automate deterministic business logic.
-   Mock external AI/notification services in most automated tests.
-   Keep a small live integration smoke test.
-   Test AI for structured/semantic correctness, not exact prose.
-   Separate AI extraction tests from scoring tests.
-   Use many unit tests, fewer integration tests, and a small critical
    E2E suite.
-   Manual n8n/UI checks are acceptable initially when documented.

## 3. Backend/API Tests

Test:

-   `/health`
-   Valid lead request
-   Missing fields
-   Invalid field types
-   Malformed JSON
-   Invalid IDs
-   Duplicate/idempotent request
-   n8n unavailable
-   Database unavailable
-   AI/workflow timeout propagation
-   Response schema/status codes

## 4. Database Tests

Test:

-   Migration up
-   Lead insertion
-   Lead retrieval
-   Constraints
-   Nullable fields
-   Score range
-   Category consistency
-   Persistence
-   Duplicate strategy

## 5. AI Tests

Required cases:

1.  Buy 3-bed Lekki, ₦80m, within 3 months
2.  Rent 2-bed Ikeja
3.  Land Ibadan below ₦20m
4.  Incomplete information
5.  HUMAN_AGENT
6.  Ambiguous budget
7.  Duplicate-message guard at system level

Assertions should focus on fields and meaning, not exact wording.

## 6. Qualification Tests

Boundary cases:

``` text
0
49
50
79
80
100
```

Also verify no double counting.

## 7. n8n Tests

Verify:

-   Webhook receives payload
-   Validation/normalization
-   AI step
-   Qualification
-   PostgreSQL write
-   Routing
-   Notification
-   Customer response
-   Error handling
-   Duplicate protection

## 8. Frontend Tests

Verify:

-   Form/chat rendering
-   Validation
-   Loading state
-   Success state
-   Error state
-   API request
-   Duplicate submission prevention
-   Responsive behavior

## 9. Integration Tests

Test:

``` text
React → FastAPI
FastAPI → n8n
n8n → AI
n8n/app → PostgreSQL
Qualification → Routing
Routing → Notification
```

## 10. E2E Tests

Keep 3--7 critical E2E scenarios. At minimum:

-   Complete high-intent lead
-   Incomplete lead requiring clarification
-   Human-agent escalation
-   Dependency failure/recoverable error

## 11. Regression

Run relevant regression tests after changes to:

-   API contracts
-   Database schema
-   AI prompt/schema
-   Qualification rules
-   n8n workflow
-   Frontend submission flow

## 12. Deployment Checks

Production checks:

-   Containers running
-   HTTPS works
-   Frontend loads
-   `/health` works
-   PostgreSQL connects
-   n8n production workflow active
-   Synthetic lead succeeds end-to-end
-   Notification arrives
-   Persistence works
-   Logs accessible
-   Backup works

## 13. Test Data

Use synthetic data. Do not use real customer PII unless explicitly
authorized and necessary.

## 14. Definition of Done

A task is not complete merely because code was written. Relevant tests
must run and results must be recorded in `IMPLEMENTATION.md`.
