from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.lead import LeadQualificationInput
from app.integrations.ai_provider import DisabledAIProvider
from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate
from app.services.qualification import qualify_lead
from app.services.ai_extraction import AIExtractionService


@dataclass(frozen=True)
class LeadSubmission:
    lead: Lead
    duplicate: bool
    should_dispatch: bool


class LeadService:
    def __init__(
        self,
        repository: LeadRepository | None = None,
        extractor: AIExtractionService | None = None,
    ) -> None:
        self.repository = repository or LeadRepository()
        self.extractor = extractor or AIExtractionService(
            DisabledAIProvider()
        )

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

        outcome = self.extractor.extract(payload.message)
        extracted = outcome.extraction

        name = payload.name or extracted.name
        email = payload.email or extracted.email
        phone = payload.phone or extracted.phone
        property_type = payload.property_type or extracted.property_type
        location = payload.location or extracted.location
        bedrooms = payload.bedrooms or extracted.bedrooms
        budget = (
            payload.budget
            if payload.budget is not None
            else extracted.budget
        )
        intent = payload.intent or extracted.intent
        timeline = payload.timeline or extracted.timeline

        qualification = qualify_lead(
            LeadQualificationInput(
                phone=phone,
                budget=budget,
                location=location,
                property_type=property_type,
                intent=intent,
                bedrooms=bedrooms,
                timeline=timeline,
            )
        )
        lead = Lead(
            idempotency_key=idempotency_key,
            name=name,
            email=str(email) if email else None,
            phone=phone,
            raw_enquiry=payload.message,
            property_type=property_type,
            location=location,
            bedrooms=bedrooms,
            budget=budget,
            intent=intent,
            timeline=timeline,
            lead_score=qualification.score,
            lead_category=qualification.category,
            processing_status="workflow_pending",
            human_agent=(
                extracted.human_agent or outcome.provider_failed
            ),
            missing_fields=extracted.missing_fields,
            ambiguous_fields=extracted.ambiguous_fields,
            ai_prompt_version=outcome.prompt_version,
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
