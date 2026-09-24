# Lead Qualification Specification

## Purpose

Define an explainable, deterministic scoring system. AI extracts facts; application code calculates the score and category.

## Scoring

| Confirmed rule | Points |
|---|---:|
| Phone present | 10 |
| Budget present | 20 |
| Location present | 15 |
| Property type present | 15 |
| Buying soon | 25 |
| Clear requirements | 15 |

Maximum: 100.

## Categories

- 0–49: COLD
- 50–79: WARM
- 80–100: HOT

## Buying soon

“Buying soon” means a confirmed actionable timeline no longer than 90 days.

Accepted equivalents include:

- ASAP, immediately, or now
- this week/month or next week/month
- up to 90 days
- up to 12 weeks
- up to 3 months

Missing, ambiguous, or longer timelines earn zero. Examples such as “sometime,” “later,” “next year,” and “4 months” do not qualify. The rule applies to the lead's intended property action even though the historical field name remains `buying_soon`.

## Clear requirements

The 15 points are awarded only when all three core requirements are confirmed:

1. intent
2. location
3. property type

At least one actionable detail must also be confirmed:

- bedrooms
- budget
- timeline

Missing or whitespace-only strings are not confirmed. AI must not subjectively award these points.

## Determinism and validation

- Each rule is evaluated once.
- Missing information earns zero.
- Identical validated input produces identical output.
- Scores outside 0–100 are rejected.
- Category is derived from score, never supplied by AI.
- Qualification is independently testable without calling an AI provider.

## Required tests

- Category boundaries: 0, 49, 50, 79, 80, 100
- Invalid scores: -1 and 101
- Timeline boundaries and common phrases
- Missing/whitespace values
- Clear-requirements completeness
- Complete 100-point lead
- No duplicate rule application
