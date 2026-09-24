from decimal import Decimal
from uuid import uuid4

from app.domain.lead import LeadCategory, LeadIntent
from app.models.lead import Lead
from app.schemas.lead import LeadCreate
from app.schemas.ai import AIExtractionOutcome, AIExtractionResult
from app.services.lead_service import LeadService


class FakeRepository:
    def __init__(self) -> None:
        self.by_key: dict[str, Lead] = {}

    def get_by_idempotency_key(
        self,
        session: object,
        idempotency_key: str,
    ) -> Lead | None:
        return self.by_key.get(idempotency_key)

    def add(self, session: object, lead: Lead) -> Lead:
        lead.id = uuid4()
        self.by_key[lead.idempotency_key or ""] = lead
        return lead


class FakeSession:
    def commit(self) -> None:
        pass

    def refresh(self, lead: Lead) -> None:
        pass

    def rollback(self) -> None:
        pass


class CountingExtractor:
    def __init__(self) -> None:
        self.calls = 0

    def extract(self, message: str) -> AIExtractionOutcome:
        self.calls += 1
        return AIExtractionOutcome(
            extraction=AIExtractionResult(),
            prompt_version="test-v1",
        )


def complete_payload() -> LeadCreate:
    return LeadCreate(
        name="Amina Yusuf",
        email="amina@example.com",
        phone="08000000000",
        message="I want a 3-bedroom apartment in Lekki.",
        property_type="apartment",
        location="Lekki",
        bedrooms=3,
        budget=Decimal("80000000"),
        intent=LeadIntent.BUY,
        timeline="within 3 months",
    )


def test_service_qualifies_and_persists_new_lead() -> None:
    repository = FakeRepository()
    service = LeadService(repository=repository)

    result = service.submit(
        session=FakeSession(),
        payload=complete_payload(),
        idempotency_key="request-12345",
    )

    assert not result.duplicate
    assert result.lead.lead_score == 100
    assert result.lead.lead_category is LeadCategory.HOT
    assert result.lead.processing_status == "workflow_pending"
    assert result.should_dispatch


def test_service_returns_existing_lead_for_duplicate_key() -> None:
    repository = FakeRepository()
    extractor = CountingExtractor()
    service = LeadService(
        repository=repository,
        extractor=extractor,
    )
    session = FakeSession()

    first = service.submit(
        session=session,
        payload=complete_payload(),
        idempotency_key="request-12345",
    )
    second = service.submit(
        session=session,
        payload=complete_payload(),
        idempotency_key="request-12345",
    )

    assert second.duplicate
    assert second.lead.id == first.lead.id
    assert not second.should_dispatch
    assert len(repository.by_key) == 1
    assert extractor.calls == 1


def test_failed_workflow_is_retryable_without_new_lead() -> None:
    repository = FakeRepository()
    service = LeadService(repository=repository)
    session = FakeSession()
    first = service.submit(
        session=session,
        payload=complete_payload(),
        idempotency_key="request-12345",
    )
    first.lead.processing_status = "workflow_failed"

    retry = service.submit(
        session=session,
        payload=complete_payload(),
        idempotency_key="request-12345",
    )

    assert retry.duplicate
    assert retry.should_dispatch
    assert len(repository.by_key) == 1
