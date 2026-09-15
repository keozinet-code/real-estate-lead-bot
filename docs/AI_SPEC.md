> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# AI Specification

## 1. Purpose

The AI component converts unstructured real-estate enquiries into
structured information and helps produce appropriate conversational
responses.

AI is a component of the system, not the entire system.

## 2. Responsibilities

AI may:

-   Understand natural-language enquiries
-   Extract lead/property fields
-   Identify missing information
-   Identify ambiguity
-   Classify intent where appropriate
-   Produce concise customer-facing responses
-   Summarize conversation context
-   Trigger/support `HUMAN_AGENT`

AI must not be responsible for authoritative deterministic lead scoring.

## 3. Structured Output

Target fields:

``` json
{
  "name": null,
  "email": null,
  "phone": null,
  "property_type": null,
  "location": null,
  "bedrooms": null,
  "budget": null,
  "intent": null,
  "timeline": null,
  "human_agent": false,
  "missing_fields": [],
  "ambiguous_fields": []
}
```

Exact schema must match implementation contracts.

## 4. Rules

-   Never fabricate missing customer data.
-   Use `null` or an agreed empty representation for unknown fields.
-   Preserve uncertainty.
-   Do not convert an ambiguous budget into a confident number.
-   Extract only what the message supports.
-   Prefer structured output over prose for machine processing.
-   Validate model output before using it.

## 5. Required Test Cases

### Case 1 --- Buyer

``` text
I want to buy a 3-bedroom apartment in Lekki for ₦80m within 3 months.
```

Expected core extraction:

``` text
intent = buy
bedrooms = 3
location = Lekki
budget = 80000000
timeline = 3 months
```

### Case 2 --- Rent

``` text
I need a 2-bedroom apartment to rent in Ikeja.
```

### Case 3 --- Land

``` text
I need land in Ibadan below ₦20 million.
```

### Case 4 --- Incomplete Information

The model should identify missing important information rather than
invent it.

### Case 5 --- HUMAN_AGENT

Explicit request for a person should trigger escalation.

### Case 6 --- Ambiguous Budget

Ambiguous values should be flagged for clarification.

### Case 7 --- Duplicate Message

Duplicate protection belongs to the wider system; AI should not cause
repeated side effects.

## 6. Failure Handling

Handle:

-   Timeout
-   Provider error
-   Invalid JSON
-   Missing required structured keys
-   Unexpected types
-   Refusal/unusable response

The application should fail safely and preserve the original enquiry for
recovery where appropriate.
