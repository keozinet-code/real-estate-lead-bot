from decimal import Decimal

import pytest

from app.domain.lead import LeadCategory, LeadIntent, LeadQualificationInput
from app.services.qualification import (
    classify_score,
    has_clear_requirements,
    is_buying_soon,
    qualify_lead,
)


@pytest.mark.parametrize(
    ("score", "category"),
    [
        (0, LeadCategory.COLD),
        (49, LeadCategory.COLD),
        (50, LeadCategory.WARM),
        (79, LeadCategory.WARM),
        (80, LeadCategory.HOT),
        (100, LeadCategory.HOT),
    ],
)
def test_category_boundaries(score: int, category: LeadCategory) -> None:
    assert classify_score(score) is category


@pytest.mark.parametrize("score", [-1, 101])
def test_invalid_scores_are_rejected(score: int) -> None:
    with pytest.raises(ValueError):
        classify_score(score)


@pytest.mark.parametrize(
    "timeline",
    ["ASAP", "this month", "within 90 days", "in 12 weeks", "within three months"],
)
def test_buying_soon_accepts_ninety_days_or_less(timeline: str) -> None:
    assert is_buying_soon(timeline)


@pytest.mark.parametrize(
    "timeline",
    [None, "", "4 months", "next year", "sometime"],
)
def test_buying_soon_rejects_missing_or_later_timelines(
    timeline: str | None,
) -> None:
    assert not is_buying_soon(timeline)


def test_clear_requirements_need_core_fields_and_actionable_detail() -> None:
    complete = LeadQualificationInput(
        intent=LeadIntent.BUY,
        location="Lekki",
        property_type="apartment",
        bedrooms=3,
    )
    incomplete = LeadQualificationInput(
        intent=LeadIntent.BUY,
        location="Lekki",
        bedrooms=3,
    )

    assert has_clear_requirements(complete)
    assert not has_clear_requirements(incomplete)


def test_complete_high_intent_lead_scores_one_hundred() -> None:
    lead = LeadQualificationInput(
        phone="08000000000",
        budget=Decimal("80000000"),
        location="Lekki",
        property_type="apartment",
        intent=LeadIntent.BUY,
        bedrooms=3,
        timeline="within 3 months",
    )

    result = qualify_lead(lead)

    assert result.score == 100
    assert result.category is LeadCategory.HOT
    assert len(result.matched_rules) == 6


def test_empty_lead_scores_zero_without_double_counting() -> None:
    result = qualify_lead(LeadQualificationInput(phone="   "))

    assert result.score == 0
    assert result.category is LeadCategory.COLD
    assert result.matched_rules == ()
