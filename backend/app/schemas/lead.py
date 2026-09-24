from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.domain.lead import LeadCategory, LeadIntent


class LeadCreate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    message: str = Field(min_length=1, max_length=5000)
    property_type: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=255)
    bedrooms: int | None = Field(default=None, gt=0)
    budget: Decimal | None = Field(default=None, ge=0)
    intent: LeadIntent | None = None
    timeline: str | None = Field(default=None, max_length=100)


class LeadAccepted(BaseModel):
    success: Literal[True] = True
    lead_id: UUID
    status: str
    message: str
    lead_score: int = Field(ge=0, le=100)
    lead_category: LeadCategory
    duplicate: bool = False


class ExtractedLead(BaseModel):
    property_type: str | None = None
    location: str | None = None
    bedrooms: int | None = Field(default=None, gt=0)
    budget: Decimal | None = Field(default=None, ge=0)
    intent: LeadIntent | None = None
    timeline: str | None = None
    human_agent: bool = False
