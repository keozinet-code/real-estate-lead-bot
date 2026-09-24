from collections.abc import Generator
from decimal import Decimal
from uuid import UUID

import httpx
from pydantic import BaseModel, ConfigDict, Field, SecretStr

from app.core.config import settings
from app.domain.lead import LeadCategory, LeadIntent
from app.models.lead import Lead


class N8nError(RuntimeError):
    pass


class N8nUnavailableError(N8nError):
    pass


class N8nRejectedError(N8nError):
    pass


class N8nPayload(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    lead_id: UUID
    idempotency_key: str
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    message: str
    property_type: str | None = None
    location: str | None = None
    bedrooms: int | None = None
    budget: Decimal | None = None
    intent: LeadIntent | None = None
    timeline: str | None = None
    lead_score: int = Field(ge=0, le=100)
    lead_category: LeadCategory
    human_agent: bool
    missing_fields: list[str] = Field(default_factory=list)
    ambiguous_fields: list[str] = Field(default_factory=list)
    ai_prompt_version: str | None = None

    @classmethod
    def from_lead(cls, lead: Lead) -> "N8nPayload":
        if lead.idempotency_key is None:
            raise ValueError("A workflow lead requires an idempotency key")
        return cls(
            lead_id=lead.id,
            idempotency_key=lead.idempotency_key,
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            message=lead.raw_enquiry,
            property_type=lead.property_type,
            location=lead.location,
            bedrooms=lead.bedrooms,
            budget=lead.budget,
            intent=lead.intent,
            timeline=lead.timeline,
            lead_score=lead.lead_score,
            lead_category=lead.lead_category,
            human_agent=lead.human_agent,
            missing_fields=lead.missing_fields or [],
            ambiguous_fields=lead.ambiguous_fields or [],
            ai_prompt_version=lead.ai_prompt_version,
        )


class N8nDispatchResponse(BaseModel):
    accepted: bool
    duplicate: bool = False
    workflow: str


class N8nClient:
    def __init__(
        self,
        *,
        webhook_url: str,
        webhook_token: SecretStr | None,
        timeout_seconds: float,
        enabled: bool,
        client: httpx.Client | None = None,
    ) -> None:
        self.enabled = enabled
        self.webhook_url = webhook_url
        self.webhook_token = webhook_token
        self._owns_client = client is None
        self.client = client or httpx.Client(
            timeout=httpx.Timeout(timeout_seconds)
        )

    def dispatch(self, lead: Lead) -> N8nDispatchResponse:
        if not self.enabled:
            raise RuntimeError("n8n dispatch is disabled")
        if self.webhook_token is None:
            raise RuntimeError("N8N_WEBHOOK_TOKEN is required")

        payload = N8nPayload.from_lead(lead)
        headers = {
            "X-Webhook-Token": self.webhook_token.get_secret_value(),
            "Idempotency-Key": payload.idempotency_key,
        }

        try:
            response = self.client.post(
                self.webhook_url,
                json=payload.model_dump(mode="json"),
                headers=headers,
            )
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise N8nUnavailableError(
                "The workflow service is temporarily unavailable"
            ) from exc
        except httpx.RequestError as exc:
            raise N8nUnavailableError(
                "The workflow request could not be completed"
            ) from exc

        if response.status_code >= 500:
            raise N8nUnavailableError(
                "The workflow service returned a server error"
            )
        if response.status_code >= 400:
            raise N8nRejectedError("The workflow rejected the request")

        try:
            result = N8nDispatchResponse.model_validate(response.json())
        except (ValueError, TypeError) as exc:
            raise N8nRejectedError(
                "The workflow returned an invalid response"
            ) from exc

        if not result.accepted:
            raise N8nRejectedError("The workflow did not accept the lead")
        return result

    def close(self) -> None:
        if self._owns_client:
            self.client.close()


def get_n8n_client() -> Generator[N8nClient, None, None]:
    client = N8nClient(
        webhook_url=settings.n8n_webhook_url,
        webhook_token=settings.n8n_webhook_token,
        timeout_seconds=settings.n8n_timeout_seconds,
        enabled=settings.n8n_enabled,
    )
    try:
        yield client
    finally:
        client.close()
