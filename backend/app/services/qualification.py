import re

from app.domain.lead import (
    LeadCategory,
    LeadQualificationInput,
    QualificationResult,
)

POINTS = {
    "phone": 10,
    "budget": 20,
    "location": 15,
    "property_type": 15,
    "buying_soon": 25,
    "clear_requirements": 15,
}

_IMMEDIATE_TIMELINES = {
    "asap",
    "immediately",
    "now",
    "this week",
    "this month",
    "next week",
    "next month",
}
_NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}
_DURATION = re.compile(
    r"(?:within|in)?\s*"
    r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    r"\s*(day|week|month)s?\b"
)


def _present(value: str | None) -> bool:
    return bool(value and value.strip())


def is_buying_soon(timeline: str | None) -> bool:
    """Return true only for a confirmed timeline of 90 days or less."""
    if not _present(timeline):
        return False

    normalized = " ".join(timeline.lower().split())
    if normalized in _IMMEDIATE_TIMELINES:
        return True

    match = _DURATION.search(normalized)
    if not match:
        return False

    raw_amount, unit = match.groups()
    amount = int(raw_amount) if raw_amount.isdigit() else _NUMBER_WORDS[raw_amount]
    limits = {"day": 90, "week": 12, "month": 3}
    return amount <= limits[unit]


def has_clear_requirements(lead: LeadQualificationInput) -> bool:
    """Require three core fields plus at least one actionable detail."""
    core_fields = (
        lead.intent is not None,
        _present(lead.location),
        _present(lead.property_type),
    )
    actionable_detail = (
        lead.bedrooms is not None
        or lead.budget is not None
        or _present(lead.timeline)
    )
    return all(core_fields) and actionable_detail


def classify_score(score: int) -> LeadCategory:
    if not 0 <= score <= 100:
        raise ValueError("Lead score must be between 0 and 100")
    if score >= 80:
        return LeadCategory.HOT
    if score >= 50:
        return LeadCategory.WARM
    return LeadCategory.COLD


def qualify_lead(lead: LeadQualificationInput) -> QualificationResult:
    matched: list[str] = []

    if _present(lead.phone):
        matched.append("phone")
    if lead.budget is not None:
        matched.append("budget")
    if _present(lead.location):
        matched.append("location")
    if _present(lead.property_type):
        matched.append("property_type")
    if is_buying_soon(lead.timeline):
        matched.append("buying_soon")
    if has_clear_requirements(lead):
        matched.append("clear_requirements")

    score = sum(POINTS[rule] for rule in matched)
    return QualificationResult(
        score=score,
        category=classify_score(score),
        matched_rules=tuple(matched),
    )
