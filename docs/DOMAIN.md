> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# Domain Specification

## 1. Domain Overview

The central domain object is a **Lead**: a person or organisation that
may potentially become a real-estate customer.

## 2. Core Concepts

### Lead

A prospective customer with contact details and property requirements.

### Property Requirement

The customer's expressed need, including property type, location,
bedrooms, budget, intent, and timeline.

### Enquiry

The raw customer message or form submission received by the system.

### Qualification

The deterministic process that assigns a score and HOT/WARM/COLD
category.

### Sales Notification

A message sent to the sales team after processing according to routing
rules.

### Human Escalation

A state in which the automated flow should hand the conversation or lead
to a human agent.

## 3. Lead Fields

  Field           Meaning
  --------------- ----------------------------------
  name            Customer name
  email           Customer email
  phone           Customer phone
  property_type   Requested property type
  location        Preferred property location
  bedrooms        Number of bedrooms when relevant
  budget          Customer budget
  intent          buy, rent, sell, or land
  timeline        Expected transaction timeline

## 4. Business Rules

-   Unknown information must remain unknown; AI must not invent it.
-   A lead can exist even when some fields are missing.
-   Qualification should use only confirmed data.
-   Scores must not be double-counted.
-   Score boundaries are deterministic.
-   Explicit requests for a human should trigger `HUMAN_AGENT`.
-   Duplicate requests should not create uncontrolled duplicate
    processing.

## 5. Qualification Categories

``` text
0–49   COLD
50–79  WARM
80–100 HOT
```

## 6. Example

Input:

``` text
I want to buy a 3-bedroom apartment in Lekki.
My budget is ₦80 million and I want to buy within three months.
```

Expected domain interpretation:

``` text
intent: buy
property_type: apartment
bedrooms: 3
location: Lekki
budget: 80000000
timeline: 3 months
```

Contact fields remain missing unless supplied.
