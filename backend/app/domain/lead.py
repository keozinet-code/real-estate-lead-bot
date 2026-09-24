from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class LeadIntent(str, Enum):
    BUY = "buy"
    RENT = "rent"
    SELL = "sell"
    LAND = "land"


class LeadCategory(str, Enum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"


@dataclass(frozen=True)
class LeadQualificationInput:
    phone: str | None = None
    budget: Decimal | None = None
    location: str | None = None
    property_type: str | None = None
    intent: LeadIntent | None = None
    bedrooms: int | None = None
    timeline: str | None = None


@dataclass(frozen=True)
class QualificationResult:
    score: int
    category: LeadCategory
    matched_rules: tuple[str, ...]
