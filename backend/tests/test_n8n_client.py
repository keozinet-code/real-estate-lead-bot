from decimal import Decimal
from uuid import uuid4

import httpx
import pytest
from pydantic import SecretStr

from app.domain.lead import LeadCategory, LeadIntent
from app.integrations.n8n_client import (
    N8nClient,
    N8nRejectedError,
    N8nUnavailableError,
)
from app.models.lead import Lead


def sample_lead() -> Lead:
    return Lead(
        id=uuid4(),
        idempotency_key="request-12345",
        name="Amina Yusuf",
        email="amina@example.com",
        phone="08000000000",
        raw_enquiry="I need a 3-bedroom apartment in Lekki.",
        property_type="apartment",
        location="Lekki",
        bedrooms=3,
        budget=Decimal("80000000"),
        intent=LeadIntent.BUY,
        timeline="within 3 months",
        lead_score=100,
        lead_category=LeadCategory.HOT,
        processing_status="workflow_pending",
        human_agent=False,
    )


def make_client(handler: object) -> N8nClient:
    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport)
    return N8nClient(
        webhook_url="https://n8n.example.test/webhook/lead-intake-v1",
        webhook_token=SecretStr("test-token"),
        timeout_seconds=3,
        enabled=True,
        client=http_client,
    )


def test_dispatch_sends_allow_list_and_auth_headers() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = __import__("json").loads(request.content)
        assert request.headers["X-Webhook-Token"] == "test-token"
        assert request.headers["Idempotency-Key"] == "request-12345"
        assert body["lead_id"]
        assert body["lead_category"] == "HOT"
        assert "database_url" not in body
        return httpx.Response(
            200,
            json={
                "accepted": True,
                "duplicate": False,
                "workflow": "lead-intake-v1",
            },
        )

    result = make_client(handler).dispatch(sample_lead())

    assert result.accepted
    assert not result.duplicate


def test_server_error_is_safe_unavailable_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="internal details")

    with pytest.raises(N8nUnavailableError):
        make_client(handler).dispatch(sample_lead())


def test_invalid_response_is_rejected() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"unexpected": True})

    with pytest.raises(N8nRejectedError):
        make_client(handler).dispatch(sample_lead())
