> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# API Specification

## 1. Purpose

Define the MVP interface between the React frontend and FastAPI backend.

## 2. Base URL

Local example:

``` text
http://localhost:8000
```

Production example:

``` text
https://api.example.com
```

## 3. Health Endpoint

### `GET /health`

Response:

``` json
{
  "status": "ok"
}
```

HTTP status: `200`.

## 4. Submit Lead / Enquiry

Recommended MVP endpoint:

### `POST /api/v1/leads`

Example request:

``` json
{
  "name": "Amina Yusuf",
  "email": "amina@example.com",
  "phone": "08000000000",
  "message": "I want to buy a 3-bedroom apartment in Lekki. My budget is ₦80 million and I want to buy within three months."
}
```

The backend should accept incomplete optional lead details because AI
may extract information from `message`.

Example successful response:

``` json
{
  "success": true,
  "lead_id": "uuid",
  "status": "processed",
  "message": "Your enquiry has been received."
}
```

The final response schema must be kept synchronized with the frontend
and implementation.

## 5. Validation

Reject or safely handle:

-   Malformed JSON
-   Invalid field types
-   Invalid email when supplied
-   Empty enquiry
-   Oversized payloads
-   Unsupported values where constrained

## 6. Error Responses

Recommended shape:

``` json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request could not be processed."
  }
}
```

Do not expose stack traces, database credentials, API keys, or internal
secrets.

## 7. Status Codes

Use appropriate HTTP status codes, including:

-   `200` / `201` success
-   `400` bad request
-   `422` validation error
-   `404` resource not found where relevant
-   `409` conflict/duplicate where applicable
-   `500` unexpected server failure
-   `502`/`503` dependency unavailable where appropriate

## 8. n8n Integration

FastAPI should call the configured production n8n webhook using an
environment variable rather than a hardcoded URL.

The integration should define:

-   Timeout
-   Authentication where required
-   Payload contract
-   Response contract
-   Retry/error behavior

## 9. Idempotency

Duplicate customer submissions must not cause uncontrolled duplicate
records or notifications. Implement an idempotency/message identifier
strategy during development.

## 10. CORS

Production CORS should allow only the required frontend origin(s), not
unrestricted origins.
