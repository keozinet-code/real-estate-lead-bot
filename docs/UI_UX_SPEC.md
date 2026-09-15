> **Project:** Real Estate Lead Bot\
> **Level:** Beginner → Intermediate MVP\
> **Stack:** React, FastAPI, PostgreSQL, n8n, AI\
> **Production target:** Existing VPS using Docker Compose and Nginx

# UI/UX Specification

## 1. Goal

Provide a simple, responsive interface that lets a customer submit a
property enquiry and clearly understand whether the request is being
processed.

## 2. Primary Experience

The MVP may use a lead form, chat-like interface, or a simple
combination of both.

Required information should be collected without making the interface
unnecessarily long.

## 3. Core UI States

The frontend must support:

-   Default/ready
-   Input validation
-   Submitting/loading
-   Success
-   Recoverable error
-   Network/server error

## 4. Inputs

The UI may collect:

-   Name
-   Email
-   Phone
-   Free-text property enquiry

Structured property fields may also be added where useful, but the AI
should still support natural-language extraction.

## 5. Validation

-   Do not submit an empty enquiry.
-   Validate email format when supplied.
-   Provide understandable field-level feedback.
-   Prevent accidental rapid duplicate submission.
-   Do not expose internal API errors to customers.

## 6. Customer Response

Responses should be:

-   Brief
-   Clear
-   Professional
-   Relevant to the enquiry
-   Explicit when more information is needed
-   Clear when a human agent will follow up

## 7. Responsive Design

The interface must work on:

-   Mobile
-   Tablet
-   Desktop

## 8. Accessibility

MVP baseline:

-   Associated form labels
-   Keyboard-accessible controls
-   Visible focus states
-   Sufficient contrast
-   Clear error text
-   Semantic HTML

## 9. Integration

React should call FastAPI using the configured API base URL.

Production API endpoints must come from environment/build configuration
rather than being hardcoded.
