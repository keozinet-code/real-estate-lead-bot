from typing import Any

import pytest

from app.domain.lead import LeadIntent
from app.services.ai_extraction import (
    AIExtractionService,
    PROMPT_VERSION,
)


class FakeProvider:
    enabled = True

    def __init__(self, output: dict[str, Any]) -> None:
        self.output = output

    def extract(
        self,
        *,
        system_prompt: str,
        customer_message: str,
    ) -> dict[str, Any]:
        assert "Do not calculate a lead score" in system_prompt
        assert customer_message
        return self.output


def base_output(**updates: Any) -> dict[str, Any]:
    output: dict[str, Any] = {
        "name": None,
        "email": None,
        "phone": None,
        "property_type": None,
        "location": None,
        "bedrooms": None,
        "budget": None,
        "intent": None,
        "timeline": None,
        "human_agent": False,
        "missing_fields": [],
        "ambiguous_fields": [],
    }
    output.update(updates)
    return output


@pytest.mark.parametrize(
    ("message", "output", "assertion"),
    [
        (
            "Buy 3-bed apartment in Lekki for ₦80m in 3 months.",
            base_output(
                property_type="apartment",
                location="Lekki",
                bedrooms=3,
                budget=80000000,
                intent="buy",
                timeline="3 months",
            ),
            ("intent", LeadIntent.BUY),
        ),
        (
            "I need a 2-bedroom apartment to rent in Ikeja.",
            base_output(
                property_type="apartment",
                location="Ikeja",
                bedrooms=2,
                intent="rent",
            ),
            ("intent", LeadIntent.RENT),
        ),
        (
            "I need land in Ibadan below ₦20 million.",
            base_output(
                property_type="land",
                location="Ibadan",
                budget=20000000,
                intent="land",
            ),
            ("location", "Ibadan"),
        ),
        (
            "I need a property.",
            base_output(
                missing_fields=[
                    "property_type",
                    "location",
                    "budget",
                    "intent",
                ]
            ),
            ("budget", None),
        ),
        (
            "Please connect me to a human agent.",
            base_output(human_agent=True),
            ("human_agent", True),
        ),
        (
            "My budget is around 20 or maybe 30 million.",
            base_output(
                budget=None,
                ambiguous_fields=["budget"],
            ),
            ("budget", None),
        ),
    ],
)
def test_documented_extraction_cases(
    message: str,
    output: dict[str, Any],
    assertion: tuple[str, Any],
) -> None:
    result = AIExtractionService(FakeProvider(output)).extract(message)

    assert getattr(result.extraction, assertion[0]) == assertion[1]
    assert result.prompt_version == PROMPT_VERSION
    assert not result.provider_failed


def test_invalid_ai_output_fails_safe_to_human_agent() -> None:
    invalid = base_output(
        budget=25000000,
        ambiguous_fields=["budget"],
    )

    result = AIExtractionService(FakeProvider(invalid)).extract(
        "My budget may be 20m or 30m."
    )

    assert result.provider_failed
    assert result.extraction.human_agent
    assert result.extraction.budget is None
