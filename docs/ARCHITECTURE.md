> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# System Architecture

## 1. Purpose

This document defines the high-level technical architecture and
responsibilities of each component.

## 2. Architecture

``` text
Customer
   ↓
React UI
   ↓
FastAPI Backend
   ↓
n8n Workflow Engine
   ├── AI Extraction
   ├── Lead Qualification
   ├── Database Operations
   └── Notifications
   ↓
PostgreSQL
```

Production:

``` text
Internet
↓
Domain / HTTPS
↓
Nginx
↓
Docker Compose on Existing VPS
├── React
├── FastAPI
├── PostgreSQL
└── n8n
```

## 3. Component Responsibilities

### React

-   Customer-facing enquiry interface
-   Form/chat interaction
-   Client-side validation
-   Loading, success, and error states
-   Calls FastAPI; it should not directly access PostgreSQL

### FastAPI

-   Public application API
-   Request validation
-   Response schemas
-   Business/integration boundary
-   Database access where specified
-   n8n invocation
-   Error handling and logging
-   Health endpoint

### n8n

-   Workflow orchestration
-   AI processing
-   Data normalization
-   Qualification orchestration
-   Database operations where designed
-   Routing
-   Sales notifications
-   Follow-up automation

### AI

-   Natural-language understanding
-   Structured extraction
-   Missing-information detection
-   Ambiguity handling
-   Response assistance
-   `HUMAN_AGENT` escalation support

AI must not be the authoritative implementation of deterministic
scoring.

### PostgreSQL

-   Permanent structured lead storage
-   Lead processing state where required
-   Audit-friendly timestamps
-   Queryable lead records

### Nginx

-   Public reverse proxy
-   HTTPS entry point
-   Routing to frontend, backend, and approved n8n endpoints

## 4. Design Principles

-   Keep the MVP modular but not microservice-heavy.
-   Separate probabilistic AI behavior from deterministic business
    rules.
-   Treat API/data contracts as explicit.
-   Keep PostgreSQL and n8n state persistent.
-   Prefer one VPS and Docker Compose for the MVP.
-   Record architectural changes in documentation.

## 5. Failure Boundaries

The system must handle:

-   Invalid customer payload
-   AI timeout/failure
-   Invalid AI structured output
-   n8n unavailable
-   PostgreSQL unavailable
-   Notification failure
-   Duplicate submission
-   Frontend network failure

## 6. Deployment Boundary

The application is deployed to an already available VPS. Provisioning,
operating-system installation, and general VPS administration are
outside this project's deployment scope.
