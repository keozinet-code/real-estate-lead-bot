> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# AI Coding Agent Instructions

## 1. Purpose

This file tells coding agents how to work safely and consistently in the
Real Estate Lead Bot repository.

## 2. Required Reading Order

Before modifying code:

1.  `README.md`
2.  `TASK.md`
3.  `IMPLEMENTATION.md`
4.  Relevant files under `docs/`
5.  Existing source code and tests

## 3. Core Rules

-   Do not silently change architecture.
-   Do not invent API contracts when `API_SPEC.md` defines them.
-   Do not invent database fields when `DATA_MODEL.md` defines them.
-   Do not let AI/LLM behavior replace deterministic qualification
    rules.
-   Do not mark a task complete merely because code was generated.
-   Inspect existing code before editing.
-   Preserve backward compatibility unless a task explicitly changes a
    contract.
-   Keep secrets out of source code, logs, documentation, and Git.
-   Use synthetic test data.
-   Keep the MVP simple.

## 4. Task Protocol

Before work:

``` text
Read docs
→ Identify Task ID
→ Check dependencies
→ Inspect implementation
→ Plan smallest change
```

After work:

``` text
Run tests
→ Record results
→ Update TASK.md
→ Update IMPLEMENTATION.md
→ Record files changed
→ Record issues/decisions
→ Set next task
```

## 5. Documentation as Contract

If code and documentation disagree:

1.  Do not guess.
2.  Identify the conflict.
3.  Determine whether the implementation or specification should change.
4.  Record the decision.
5.  Update affected documents and tests together.

## 6. AI Safety/Quality Rules

For lead extraction:

-   Do not fabricate customer data.
-   Preserve unknown/ambiguous values.
-   Validate structured AI output.
-   Support human escalation.
-   Avoid side effects from duplicate messages.

## 7. Deployment

Production target:

``` text
Existing VPS
→ Nginx
→ Docker Compose
   ├── React
   ├── FastAPI
   ├── PostgreSQL
   └── n8n
```

Do not introduce Kubernetes or microservices unless the architecture is
explicitly revised.
