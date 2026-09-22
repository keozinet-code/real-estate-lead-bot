from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    message: str = Field(min_length=1, max_length=5000)


class LeadAccepted(BaseModel):
    success: Literal[True] = True
    lead_id: UUID
    status: str
    message: str


class ExtractedLead(BaseModel):
    property_type: str | None = None
    location: str | None = None
    bedrooms: int | None = Field(default=None, gt=0)
    budget: Decimal | None = Field(default=None, ge=0)
    intent: Literal["buy", "rent", "sell", "land"] | None = None
    timeline: str | None = None
    human_agent: bool = False
