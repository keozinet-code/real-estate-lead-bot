from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lead import Lead


class LeadRepository:
    def get_by_idempotency_key(
        self,
        session: Session,
        idempotency_key: str,
    ) -> Lead | None:
        statement = select(Lead).where(
            Lead.idempotency_key == idempotency_key
        )
        return session.scalar(statement)

    def add(self, session: Session, lead: Lead) -> Lead:
        session.add(lead)
        session.flush()
        return lead
