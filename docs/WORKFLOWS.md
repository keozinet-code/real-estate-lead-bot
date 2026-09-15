> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# Workflow Specification

## 1. Main Workflow

``` text
Webhook
↓
Validate / Normalize
↓
AI Processing
↓
Extract Requirements
↓
Lead Qualification
↓
PostgreSQL
↓
IF / Routing
├── HOT → Priority Sales Notification
├── WARM → Standard Follow-up
└── COLD → Standard Follow-up
↓
Customer Response
```

## 2. n8n Node Responsibilities

### Webhook

Receives a validated request from FastAPI.

### Validate / Edit Fields

Normalizes expected fields and prepares a predictable payload.

### AI Processing

Extracts structured property requirements from the enquiry.

### Qualification

Applies deterministic scoring rules. This may be implemented in code or
a clearly deterministic n8n step.

### PostgreSQL

Stores the processed lead.

### IF / Routing

Routes based on category, escalation state, or processing result.

### Notification

Sends relevant lead information to the sales team.

### Response

Returns an appropriate result to the calling application/customer.

## 3. Error Workflow

Failures should be handled explicitly:

``` text
Error
↓
Log useful context
↓
Avoid duplicate processing
↓
Return safe failure result
↓
Escalate when necessary
```

## 4. HUMAN_AGENT

If the customer explicitly requests a human, or automation cannot safely
continue, set/route:

``` text
HUMAN_AGENT
```

and notify the appropriate human workflow.

## 5. Duplicate Guard

The workflow should use a request/message identifier or equivalent
strategy to avoid processing the same submission repeatedly.

## 6. Workflow Versioning

Export production workflows to:

``` text
n8n/workflows/
```

Do not commit credentials in exported JSON.

## 7. Production

Production webhooks must use production URLs and active workflow
endpoints, not n8n test webhook URLs.
