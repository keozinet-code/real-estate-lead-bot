> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# Lead Qualification Specification

## 1. Purpose

Define a simple, explainable, deterministic MVP lead scoring system.

## 2. Scoring

  Rule                      Points
  ----------------------- --------
  Phone present                 10
  Budget present                20
  Location present              15
  Property type present         15
  Buying soon                   25
  Clear requirements            15

Maximum score: `100`.

## 3. Categories

``` text
0–49   → COLD
50–79  → WARM
80–100 → HOT
```

## 4. Principles

-   Qualification must be deterministic.
-   The same validated input should produce the same score.
-   Do not let the LLM invent the final score.
-   Do not double-count a rule.
-   Only confirmed information earns points.
-   Missing information earns zero for that rule.
-   Scoring and category should be testable independently from AI.

## 5. Buying Soon

The implementation must define the exact timeline threshold for "buying
soon" before coding. Once defined, record it in this specification and
tests.

Until that threshold is explicitly agreed, do not silently invent one.

## 6. Clear Requirements

The implementation must define the deterministic criteria for "clear
requirements." Avoid asking the AI to subjectively assign these 15
points without a validated rule.

## 7. Boundary Tests

Required:

-   Score `0` → COLD
-   Score `49` → COLD
-   Score `50` → WARM
-   Score `79` → WARM
-   Score `80` → HOT
-   Score `100` → HOT

Also test:

-   Missing fields
-   No double counting
-   Invalid score prevention
-   Category always matches score

## 8. Output

Example:

``` json
{
  "lead_score": 80,
  "lead_category": "HOT"
}
```
