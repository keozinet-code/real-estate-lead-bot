> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# Product Requirements Document

## 1. Product Summary

The Real Estate Lead Bot is an MVP that receives property enquiries,
understands the customer's requirements, extracts structured lead
information, qualifies the lead, stores it, alerts the sales team, and
returns an appropriate response.

## 2. Problem

Real-estate teams can lose leads when enquiries arrive with incomplete
or unstructured information, follow-up is slow, or salespeople cannot
quickly identify high-intent prospects.

## 3. Goal

Build a simple system that converts a natural-language property enquiry
into a structured, qualified, actionable lead.

## 4. Users

-   Property buyers
-   Property renters
-   Land buyers
-   Property sellers
-   Real-estate sales agents
-   Sales managers
-   System administrators

## 5. Core User Journey

``` text
Customer
→ Chat / Lead Form
→ FastAPI
→ n8n
→ AI Extraction
→ Lead Qualification
→ PostgreSQL
→ Sales Notification
→ Customer Response
```

## 6. Lead Information

The MVP should support:

-   `name`
-   `email`
-   `phone`
-   `property_type`
-   `location`
-   `bedrooms`
-   `budget`
-   `intent`
-   `timeline`

Supported intent values include:

``` text
buy
rent
sell
land
```

## 7. Functional Requirements

The system shall:

1.  Accept a customer enquiry.
2.  Validate incoming data.
3.  Send the enquiry into the automation workflow.
4.  Extract structured property requirements using AI.
5.  Identify missing or ambiguous information.
6.  Calculate a deterministic lead score.
7.  Classify leads as HOT, WARM, or COLD.
8.  Save the lead to PostgreSQL.
9.  Notify the sales team where required.
10. Return an appropriate customer response.
11. Support `HUMAN_AGENT` escalation.
12. Guard against accidental duplicate processing.

## 8. Lead Qualification

Educational MVP scoring:

  Signal                    Score
  ----------------------- -------
  Phone present               +10
  Budget present              +20
  Location present            +15
  Property type present       +15
  Buying soon                 +25
  Clear requirements          +15

Classification:

-   `80–100` → HOT
-   `50–79` → WARM
-   `0–49` → COLD

## 9. Non-Functional Requirements

The system should be:

-   Reliable
-   Understandable
-   Maintainable
-   Secure enough for an MVP handling personal information
-   Easy to test
-   Easy to deploy
-   Observable through useful logs
-   Recoverable through backups
-   Simple enough for developers and AI coding agents to understand

## 10. MVP Success Criteria

The MVP succeeds when:

-   A customer can submit an enquiry.
-   The system understands the enquiry.
-   Important property requirements are extracted.
-   A score and category are generated.
-   The lead is stored.
-   Sales receives the required notification.
-   The customer receives an appropriate response.
-   The full flow works in production on the existing VPS.

## 11. Out of Scope

For the MVP:

-   Kubernetes
-   Microservices
-   Complex recommendation engines
-   Large-scale property marketplace functionality
-   Advanced analytics platform
-   Multi-region deployment
-   VPS provisioning and general server administration

## 12. Definition of Done

``` text
Customer
→ Production UI
→ FastAPI
→ n8n
→ AI
→ Qualification
→ PostgreSQL
→ Sales Notification
→ Customer Response
```

The complete path must be tested successfully.
