from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.lead import LeadQualificationInput
from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate
from app.services.qualification import qualify_lead


@dataclass(frozen=True)
class LeadSubmission:
    lead: Lead
    duplicate: bool
    should_dispatch: bool


class LeadService:
    def __init__(
        self,
        repository: LeadRepository | None = None,
    ) -> None:
        self.repository = repository or LeadRepository()

    def submit(
        self,
        session: Session,
        payload: LeadCreate,
        idempotency_key: str,
    ) -> LeadSubmission:
        existing = self.repository.get_by_idempotency_key(
            session,
            idempotency_key,
        )
        if existing is not None:
            return LeadSubmission(
                lead=existing,
                duplicate=True,
                should_dispatch=existing.processing_status
                == "workflow_failed",
            )

        qualification = qualify_lead(
            LeadQualificationInput(
                phone=payload.phone,
                budget=payload.budget,
                location=payload.location,
                property_type=payload.property_type,
                intent=payload.intent,
                bedrooms=payload.bedrooms,
                timeline=payload.timeline,
            )
        )
        lead = Lead(
            idempotency_key=idempotency_key,
            name=payload.name,
            email=str(payload.email) if payload.email else None,
            phone=payload.phone,
            raw_enquiry=payload.message,
            property_type=payload.property_type,
            location=payload.location,
            bedrooms=payload.bedrooms,
            budget=payload.budget,
            intent=payload.intent,
            timeline=payload.timeline,
            lead_score=qualification.score,
            lead_category=qualification.category,
            processing_status="workflow_pending",
            human_agent=False,
        )

        try:
            self.repository.add(session, lead)
            session.commit()
            session.refresh(lead)
        except IntegrityError:
            session.rollback()
            existing = self.repository.get_by_idempotency_key(
                session,
                idempotency_key,
            )
            if existing is None:
                raise
            return LeadSubmission(
                lead=existing,
                duplicate=True,
                should_dispatch=existing.processing_status
                == "workflow_failed",
            )

        return LeadSubmission(
            lead=lead,
            duplicate=False,
            should_dispatch=True,
        )

    def mark_workflow_dispatched(
        self,
        session: Session,
        lead: Lead,
    ) -> None:
        lead.processing_status = "workflow_dispatched"
        session.commit()
        session.refresh(lead)

    def mark_workflow_failed(
        self,
        session: Session,
        lead: Lead,
    ) -> None:
        lead.processing_status = "workflow_failed"
        session.commit()
        session.refresh(lead)


def get_lead_service() -> LeadService:
    return LeadService()
