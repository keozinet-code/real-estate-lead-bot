> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# Real Estate Lead Bot

An educational MVP that captures real-estate enquiries, extracts
structured requirements with AI, qualifies leads, stores them in
PostgreSQL, routes them with n8n, and supports sales follow-up.

## Architecture

``` text
Customer
→ React
→ FastAPI
→ n8n
→ AI Extraction
→ Lead Qualification
→ PostgreSQL
→ Sales Notification
→ Customer Response
```

Production runs on an existing VPS using Docker Compose and Nginx.

## Documentation

``` text
docs/
├── PRD.md
├── ARCHITECTURE.md
├── DOMAIN.md
├── DATA_MODEL.md
├── API_SPEC.md
├── WORKFLOWS.md
├── AI_SPEC.md
├── LEAD_QUALIFICATION_SPEC.md
├── UI_UX_SPEC.md
├── TESTING_SPEC.md
└── DEPLOYMENT_SPEC.md
```

Project control files:

``` text
README.md
AGENTS.md
TASK.md
IMPLEMENTATION.md
```

## Planned Repository Structure

``` text
real-estate-lead-bot/
├── README.md
├── AGENTS.md
├── TASK.md
├── IMPLEMENTATION.md
├── docker-compose.yml
├── .env.example
├── docs/
├── frontend/
├── backend/
├── database/
├── n8n/
│   └── workflows/
└── tests/
```

## Core Lead Fields

``` text
name
email
phone
property_type
location
bedrooms
budget
intent
timeline
```

## Qualification

``` text
Phone +10
Budget +20
Location +15
Property type +15
Buying soon +25
Clear requirements +15

80–100 HOT
50–79  WARM
0–49   COLD
```

## Development Workflow

1.  Read the relevant specification.
2.  Select a task from `TASK.md`.
3.  Inspect existing code before changing it.
4.  Implement the smallest coherent change.
5.  Run relevant tests.
6.  Update `TASK.md`.
7.  Record actual work in `IMPLEMENTATION.md`.

## Production

Deployment assumes an existing accessible VPS. The application stack is
deployed using Docker Compose with React, FastAPI, PostgreSQL, n8n, and
Nginx.

See `docs/DEPLOYMENT_SPEC.md`.
