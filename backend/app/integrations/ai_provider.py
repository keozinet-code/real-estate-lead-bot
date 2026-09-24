from collections.abc import Generator
from typing import Any, Protocol

import httpx
from pydantic import SecretStr

from app.core.config import settings


class AIProviderError(RuntimeError):
    pass


class StructuredAIProvider(Protocol):
    enabled: bool

    def extract(
        self,
        *,
        system_prompt: str,
        customer_message: str,
    ) -> dict[str, Any]:
        ...


class DisabledAIProvider:
    enabled = False

    def extract(
        self,
        *,
        system_prompt: str,
        customer_message: str,
    ) -> dict[str, Any]:
        return {}


class OpenAICompatibleProvider:
    def __init__(
        self,
        *,
        enabled: bool,
        endpoint_url: str,
        api_key: SecretStr | None,
        model: str | None,
        timeout_seconds: float,
        client: httpx.Client | None = None,
    ) -> None:
        self.enabled = enabled
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.model = model
        self._owns_client = client is None
        self.client = client or httpx.Client(
            timeout=httpx.Timeout(timeout_seconds)
        )

    def extract(
        self,
        *,
        system_prompt: str,
        customer_message: str,
    ) -> dict[str, Any]:
        if not self.enabled:
            return {}
        if self.api_key is None or not self.model:
            raise AIProviderError(
                "AI_API_KEY and AI_MODEL are required when AI is enabled"
            )

        try:
            response = self.client.post(
                self.endpoint_url,
                headers={
                    "Authorization": (
                        f"Bearer {self.api_key.get_secret_value()}"
                    )
                },
                json={
                    "model": self.model,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": customer_message},
                    ],
                },
            )
        except httpx.RequestError as exc:
            raise AIProviderError(
                "AI provider request failed"
            ) from exc

        if response.status_code >= 400:
            raise AIProviderError("AI provider rejected the request")

        try:
            body = response.json()
            content = body["choices"][0]["message"]["content"]
            if not isinstance(content, str):
                raise TypeError("AI content must be a JSON string")
            parsed = __import__("json").loads(content)
            if not isinstance(parsed, dict):
                raise TypeError("AI output must be an object")
            return parsed
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise AIProviderError(
                "AI provider returned an invalid response"
            ) from exc

    def close(self) -> None:
        if self._owns_client:
            self.client.close()


def get_ai_provider() -> Generator[
    OpenAICompatibleProvider,
    None,
    None,
]:
    provider = OpenAICompatibleProvider(
        enabled=settings.ai_enabled,
        endpoint_url=settings.ai_endpoint_url,
        api_key=settings.ai_api_key,
        model=settings.ai_model,
        timeout_seconds=settings.ai_timeout_seconds,
    )
    try:
        yield provider
    finally:
        provider.close()
