from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1.leads import get_configured_lead_service
from app.db.base import Base
from app.db.session import get_db
from app.integrations.n8n_client import get_n8n_client
from app.main import app
from app.models.lead import Lead
from app.services.lead_service import LeadService


engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, expire_on_commit=False)


class DisabledN8nClient:
    enabled = False


def override_db() -> Generator[Session, None, None]:
    with TestingSession() as session:
        yield session


def configured_service() -> LeadService:
    return LeadService()


def setup_module() -> None:
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_configured_lead_service] = configured_service
    app.dependency_overrides[get_n8n_client] = DisabledN8nClient


def teardown_module() -> None:
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_api_persists_qualified_lead_and_deduplicates_retry() -> None:
    client = TestClient(app)
    headers = {"Idempotency-Key": "integration-lead-001"}
    payload = {
        "name": "Amina Yusuf",
        "phone": "08000000000",
        "message": "I want to buy a 3-bedroom apartment in Lekki within 3 months.",
        "property_type": "apartment",
        "location": "Lekki",
        "bedrooms": 3,
        "budget": 80000000,
        "intent": "buy",
        "timeline": "within 3 months",
    }

    created = client.post("/api/v1/leads", headers=headers, json=payload)
    duplicate = client.post("/api/v1/leads", headers=headers, json=payload)

    assert created.status_code == 201
    assert created.json()["lead_category"] == "HOT"
    assert duplicate.status_code == 200
    assert duplicate.json()["duplicate"] is True
    assert duplicate.json()["lead_id"] == created.json()["lead_id"]

    with TestingSession() as session:
        leads = session.scalars(select(Lead)).all()
        assert len(leads) == 1
        assert leads[0].idempotency_key == "integration-lead-001"
