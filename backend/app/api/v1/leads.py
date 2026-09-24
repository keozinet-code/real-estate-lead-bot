from typing import Annotated

from fastapi import APIRouter, Depends, Header, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.lead import LeadAccepted, LeadCreate
from app.services.lead_service import LeadService, get_lead_service

router = APIRouter(prefix="/leads", tags=["leads"])

IdempotencyKey = Annotated[
    str,
    Header(
        alias="Idempotency-Key",
        min_length=8,
        max_length=128,
        pattern=r"^[A-Za-z0-9._:-]+$",
    ),
]


@router.post(
    "",
    response_model=LeadAccepted,
    status_code=status.HTTP_201_CREATED,
)
def submit_lead(
    payload: LeadCreate,
    response: Response,
    idempotency_key: IdempotencyKey,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[LeadService, Depends(get_lead_service)],
) -> LeadAccepted:
    submission = service.submit(
        session=session,
        payload=payload,
        idempotency_key=idempotency_key,
    )
    if submission.duplicate:
        response.status_code = status.HTTP_200_OK

    lead = submission.lead
    return LeadAccepted(
        lead_id=lead.id,
        status=lead.processing_status,
        message=(
            "Your enquiry has already been received."
            if submission.duplicate
            else "Your enquiry has been received."
        ),
        lead_score=lead.lead_score,
        lead_category=lead.lead_category,
        duplicate=submission.duplicate,
    )
