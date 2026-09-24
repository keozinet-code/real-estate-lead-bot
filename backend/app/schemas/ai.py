from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.domain.lead import LeadIntent

ExtractableField = Literal[
    "name",
    "email",
    "phone",
    "property_type",
    "location",
    "bedrooms",
    "budget",
    "intent",
    "timeline",
]


class AIExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    property_type: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=255)
    bedrooms: int | None = Field(default=None, gt=0)
    budget: Decimal | None = Field(default=None, ge=0)
    intent: LeadIntent | None = None
    timeline: str | None = Field(default=None, max_length=100)
    human_agent: bool = False
    missing_fields: list[ExtractableField] = Field(default_factory=list)
    ambiguous_fields: list[ExtractableField] = Field(default_factory=list)

    @model_validator(mode="after")
    def preserve_ambiguity(self) -> "AIExtractionResult":
        for field_name in self.ambiguous_fields:
            if getattr(self, field_name) is not None:
                raise ValueError(
                    f"Ambiguous field must be null: {field_name}"
                )
        self.missing_fields = list(dict.fromkeys(self.missing_fields))
        self.ambiguous_fields = list(
            dict.fromkeys(self.ambiguous_fields)
        )
        return self


class AIExtractionOutcome(BaseModel):
    extraction: AIExtractionResult
    prompt_version: str
    provider_failed: bool = False
