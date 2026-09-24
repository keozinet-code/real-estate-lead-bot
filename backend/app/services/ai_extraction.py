from importlib.resources import files

from pydantic import ValidationError

from app.integrations.ai_provider import (
    AIProviderError,
    StructuredAIProvider,
)
from app.schemas.ai import AIExtractionOutcome, AIExtractionResult

PROMPT_VERSION = "lead-extraction-v1"


class AIExtractionService:
    def __init__(self, provider: StructuredAIProvider) -> None:
        self.provider = provider
        self.system_prompt = (
            files("app.prompts")
            .joinpath("lead_extraction_v1.txt")
            .read_text(encoding="utf-8")
        )

    def extract(self, message: str) -> AIExtractionOutcome:
        if not self.provider.enabled:
            return AIExtractionOutcome(
                extraction=AIExtractionResult(),
                prompt_version=PROMPT_VERSION,
            )

        try:
            raw = self.provider.extract(
                system_prompt=self.system_prompt,
                customer_message=message,
            )
            extraction = AIExtractionResult.model_validate(raw)
        except (AIProviderError, ValidationError, ValueError, TypeError):
            return AIExtractionOutcome(
                extraction=AIExtractionResult(human_agent=True),
                prompt_version=PROMPT_VERSION,
                provider_failed=True,
            )

        return AIExtractionOutcome(
            extraction=extraction,
            prompt_version=PROMPT_VERSION,
        )
