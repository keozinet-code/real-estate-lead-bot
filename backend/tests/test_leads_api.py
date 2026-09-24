from dataclasses import dataclass
from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.session import get_db
from app.domain.lead import LeadCategory
from app.main import app
from app.services.lead_service import get_lead_service


@dataclass
class StubLead:
    id: object
    processing_status: str
    lead_score: int
    lead_category: LeadCategory


@dataclass
class StubSubmission:
    lead: StubLead
    duplicate: bool


class StubService:
    def __init__(self, duplicate: bool = False) -> None:
        self.duplicate = duplicate

    def submit(self, **kwargs: object) -> StubSubmission:
        return StubSubmission(
            lead=StubLead(
                id=uuid4(),
                processing_status="qualified",
                lead_score=100,
                lead_category=LeadCategory.HOT,
            ),
            duplicate=self.duplicate,
        )


def fake_db() -> object:
    yield object()


def request_body() -> dict[str, object]:
    return {
        "name": "Amina Yusuf",
        "email": "amina@example.com",
        "phone": "08000000000",
        "message": "I want a 3-bedroom apartment in Lekki.",
        "property_type": "apartment",
        "location": "Lekki",
        "bedrooms": 3,
        "budget": 80000000,
        "intent": "buy",
        "timeline": "within 3 months",
    }


def test_create_lead_returns_201() -> None:
    app.dependency_overrides[get_db] = fake_db
    app.dependency_overrides[get_lead_service] = lambda: StubService()
    client = TestClient(app)

    response = client.post(
        "/api/v1/leads",
        headers={"Idempotency-Key": "request-12345"},
        json=request_body(),
    )

    app.dependency_overrides.clear()
    assert response.status_code == 201
    assert response.json()["lead_score"] == 100
    assert response.json()["lead_category"] == "HOT"
    assert response.json()["duplicate"] is False


def test_duplicate_lead_returns_original_with_200() -> None:
    app.dependency_overrides[get_db] = fake_db
    app.dependency_overrides[get_lead_service] = lambda: StubService(
        duplicate=True
    )
    client = TestClient(app)

    response = client.post(
        "/api/v1/leads",
        headers={"Idempotency-Key": "request-12345"},
        json=request_body(),
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["duplicate"] is True


def test_missing_idempotency_key_is_rejected() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/leads", json=request_body())

    assert response.status_code == 422
