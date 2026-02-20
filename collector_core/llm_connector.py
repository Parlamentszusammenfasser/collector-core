from __future__ import annotations

import asyncio
import logging
import time
from collections import deque
from enum import StrEnum
from typing import Any, Final

import litellm

LOGGER = logging.getLogger(__name__)

RATE_LIMIT_MAX_CALLS: int | None = 20
RATE_LIMIT_WINDOW_SECONDS: int = 30


class LLMProvider(StrEnum):
    OPENAI = "openai"
    CLAUDE = "claude"
    MISTRAL = "mistral"
    BEDROCK = "bedrock"


DEFAULT_MODELS: Final[dict[LLMProvider, str]] = {
    LLMProvider.OPENAI: "openai/gpt-4o-mini",
    LLMProvider.CLAUDE: "anthropic/claude-3-5-haiku-latest",
    LLMProvider.MISTRAL: "mistral/mistral-small-latest",
    LLMProvider.BEDROCK: "bedrock/anthropic.claude-3-5-haiku-20241022-v1:0",
}

DEFAULT_SYSTEM_PROMPT: Final[str] = (
    "Du bist ein präziser Assistent. Antworte klar, faktenorientiert und auf Deutsch."
)


class LLMConnectorError(RuntimeError):
    """Raised when a provider response cannot be parsed as text."""


class AsyncRateLimiter:
    """Limit async calls to `max_calls` within `per_seconds`."""

    def __init__(self, max_calls: int, per_seconds: float) -> None:
        if max_calls <= 0:
            raise ValueError("max_calls must be greater than 0")
        if per_seconds <= 0:
            raise ValueError("per_seconds must be greater than 0")

        self.max_calls = max_calls
        self.per_seconds = float(per_seconds)
        self._timestamps: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire_slot(self) -> None:
        while True:
            async with self._lock:
                now = time.monotonic()
                cutoff = now - self.per_seconds

                while self._timestamps and self._timestamps[0] <= cutoff:
                    self._timestamps.popleft()

                if len(self._timestamps) < self.max_calls:
                    self._timestamps.append(now)
                    return

                wait_seconds = self.per_seconds - (now - self._timestamps[0])

            await asyncio.sleep(max(wait_seconds, 0.0))


class LLMConnector:
    """Thin provider-agnostic connector for text generation via LiteLLM."""

    def __init__(
        self,
        provider: LLMProvider | str,
        model: str | None = None,
        response_creativity: float = 0.2,
        rate_limit_max_calls: int | None = RATE_LIMIT_MAX_CALLS,
        rate_limit_window_seconds: float = RATE_LIMIT_WINDOW_SECONDS,
    ) -> None:
        """Initialize a provider-specific text generation connector.

        Args:
            provider: Target LLM provider (`openai`, `claude`, `mistral`, `bedrock`).
            model: Optional model override. If omitted, a provider default is used.
            response_creativity: Creativity/randomness of generated text (maps to provider
                temperature). Lower values are more deterministic.
            rate_limit_max_calls: Optional max number of async calls in the configured time window.
            rate_limit_window_seconds: Length of the async rate-limit window in seconds.
        """
        self.provider = self._parse_provider(provider)
        self.model = model.strip() if model else DEFAULT_MODELS[self.provider]
        self.response_creativity = float(response_creativity)
        self._rate_limiter = (
            AsyncRateLimiter(max_calls=rate_limit_max_calls, per_seconds=rate_limit_window_seconds)
            if rate_limit_max_calls is not None
            else None
        )

    async def generate_text(self, prompt: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
        if self._rate_limiter is not None:
            await self._rate_limiter.acquire_slot()

        request_kwargs = self._build_request(prompt=prompt, system_prompt=system_prompt)
        response = await litellm.acompletion(**request_kwargs)
        return self._extract_text(response)

    def _build_request(self, prompt: str, system_prompt: str) -> dict[str, Any]:
        user_prompt = prompt.strip()
        if not user_prompt:
            raise ValueError("prompt must not be empty")

        messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return {
            "model": self.model,
            "messages": messages,
            "temperature": self.response_creativity,
        }

    async def summarize(self, text: str, max_sentences: int = 5, language: str = "Deutsch") -> str:
        source_text = text.strip()
        if not source_text:
            raise ValueError("text must not be empty")

        prompt = (
            f"Fasse den folgenden Text in {language} zusammen. "
            f"Nenne nur die Kernaussagen in maximal {max_sentences} Sätzen.\n\n{source_text}"
        )
        summary_system_prompt = (
            "Du bist ein Assistent für politische und juristische Texte. "
            "Schreibe nüchtern, präzise und ohne Spekulation."
        )
        return await self.generate_text(prompt=prompt, system_prompt=summary_system_prompt)

    @staticmethod
    def _parse_provider(provider: LLMProvider | str) -> LLMProvider:
        if isinstance(provider, LLMProvider):
            return provider

        normalized = provider.strip().lower()
        try:
            return LLMProvider(normalized)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in LLMProvider)
            raise ValueError(f"unsupported provider '{provider}', expected one of: {allowed}") from exc

    @staticmethod
    def _extract_text(response: Any) -> str:
        choices = LLMConnector._get_field(response, "choices")
        if not isinstance(choices, list) or not choices:
            raise LLMConnectorError("provider response did not contain choices")

        message = LLMConnector._get_field(choices[0], "message")
        content = LLMConnector._get_field(message, "content")
        text = LLMConnector._normalize_content(content)
        if not text:
            raise LLMConnectorError("provider response did not contain text content")
        return text

    @staticmethod
    def _normalize_content(content: Any) -> str:
        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, str):
                    item_text = item.strip()
                    if item_text:
                        parts.append(item_text)
                    continue

                item_text = LLMConnector._get_field(item, "text")
                if isinstance(item_text, str):
                    cleaned = item_text.strip()
                    if cleaned:
                        parts.append(cleaned)
            return "\n".join(parts).strip()

        LOGGER.warning("Unexpected content type from provider: %s", type(content).__name__)
        return ""

    @staticmethod
    def _get_field(obj: Any, field: str) -> Any:
        if isinstance(obj, dict):
            return obj.get(field)
        return getattr(obj, field, None)
