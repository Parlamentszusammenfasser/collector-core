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
REQUEST_TIMEOUT_SECONDS: float = 60.0
MAX_RETRIES: int = 2
RETRY_BASE_DELAY_SECONDS: float = 0.5
RETRY_MAX_DELAY_SECONDS: float = 8.0


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


class LLMProviderError(LLMConnectorError):
    """Raised when the LLM provider returns a known request/response failure."""


class LLMAuthenticationError(LLMProviderError):
    """Raised when provider authentication fails (e.g., invalid or missing API key)."""


class LLMQuotaExceededError(LLMProviderError):
    """Raised when provider quota/budget is exhausted."""


class LLMRateLimitError(LLMProviderError):
    """Raised when provider-side rate limits are exceeded."""


class LLMTemporaryProviderError(LLMProviderError):
    """Raised for transient provider failures (timeout/5xx)."""


class RateLimiter:
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
        timeout_seconds: float = REQUEST_TIMEOUT_SECONDS,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        """Initialize a provider-specific text generation connector.

        Args:
            provider: Target LLM provider (`openai`, `claude`, `mistral`, `bedrock`).
            model: Optional model override. If omitted, a provider default is used.
            response_creativity: Creativity/randomness of generated text (maps to provider
                temperature). Lower values are more deterministic.
            rate_limit_max_calls: Optional max number of async calls in the configured time window.
            rate_limit_window_seconds: Length of the async rate-limit window in seconds.
            timeout_seconds: Timeout per provider call in seconds.
            max_retries: Number of retry attempts for retryable provider errors.
        """
        self.provider = self._parse_provider(provider)
        self.model = (
            self._require_non_empty_text(model, field_name="model")
            if model is not None
            else DEFAULT_MODELS[self.provider]
        )
        self.response_creativity = self._validate_response_creativity(response_creativity)
        self._validate_rate_limit_configuration(
            rate_limit_max_calls=rate_limit_max_calls,
            rate_limit_window_seconds=rate_limit_window_seconds,
        )
        self.timeout_seconds: float = self._validate_timeout_seconds(timeout_seconds)
        self.max_retries: int = self._validate_max_retries(max_retries)
        self.retry_base_delay_seconds: float = RETRY_BASE_DELAY_SECONDS
        self.retry_max_delay_seconds: float = RETRY_MAX_DELAY_SECONDS
        self._validate_retry_delay_constants()
        self._rate_limiter = (
            RateLimiter(max_calls=rate_limit_max_calls, per_seconds=rate_limit_window_seconds)
            if rate_limit_max_calls is not None
            else None
        )

    async def generate_text(self, prompt: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
        request_kwargs = self._build_request(prompt=prompt, system_prompt=system_prompt)
        for attempt in range(self.max_retries + 1):
            if self._rate_limiter is not None:
                await self._rate_limiter.acquire_slot()

            try:
                response = await asyncio.wait_for(
                    litellm.acompletion(**request_kwargs), timeout=self.timeout_seconds
                )
                return self._extract_text(response)
            except asyncio.TimeoutError as exc:
                mapped_error: LLMProviderError = LLMTemporaryProviderError(
                    "provider request timed out"
                )
                original_error: Exception = exc
            except Exception as exc:
                mapped_error = self._map_provider_exception(exc)
                original_error = exc

            should_retry: bool = attempt < self.max_retries and self._is_retryable_error(mapped_error)
            if not should_retry:
                raise mapped_error from original_error

            # Compute and apply exponential backoff delay before next retry attempt
            delay = self.retry_base_delay_seconds * (2 ** attempt)
            backoff_seconds = float(min(delay, self.retry_max_delay_seconds))

            await asyncio.sleep(backoff_seconds)

        raise LLMConnectorError("unreachable retry loop state")

    def _build_request(self, prompt: str, system_prompt: str) -> dict[str, Any]:
        user_prompt = self._require_non_empty_text(prompt, field_name="prompt")
        normalized_system_prompt = self._require_non_empty_text(
            system_prompt, field_name="system_prompt"
        )

        messages: list[dict[str, str]] = [
            {"role": "system", "content": normalized_system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return {
            "model": self.model,
            "messages": messages,
            "temperature": self.response_creativity,
        }

    async def summarize(self, text: str, max_sentences: int = 5, language: str = "Deutsch") -> str:
        source_text = self._require_non_empty_text(text, field_name="text")
        normalized_language = self._require_non_empty_text(language, field_name="language")
        if max_sentences <= 0:
            raise ValueError("max_sentences must be greater than 0")

        prompt = (
            f"Fasse den folgenden Text in {normalized_language} zusammen. "
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

        if not isinstance(provider, str):
            raise ValueError("provider must be an LLMProvider or non-empty string")

        normalized = provider.strip().lower()
        if not normalized:
            raise ValueError("provider must not be empty")
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

    @staticmethod
    def _map_provider_exception(exc: Exception) -> LLMProviderError:
        status_code = LLMConnector._extract_status_code(exc)
        message = str(exc).lower()

        if status_code in (401, 403) or any(
            token in message
            for token in ("unauthenticated", "unauthorized", "authentication", "invalid api key")
        ):
            return LLMAuthenticationError("provider authentication failed")

        if (
            status_code == 402
            or "insufficient_quota" in message
            or "quota exceeded" in message
            or "budget" in message
        ):
            return LLMQuotaExceededError("provider quota or budget exhausted")

        if status_code == 429 or "rate limit" in message or "too many requests" in message:
            return LLMRateLimitError("provider rate limit exceeded")

        if status_code in (408, 500, 502, 503, 504) or any(
            token in message for token in ("timeout", "timed out", "temporarily unavailable")
        ):
            return LLMTemporaryProviderError("temporary provider failure")

        return LLMProviderError(f"provider request failed: {exc}")

    @staticmethod
    def _extract_status_code(exc: Exception) -> int | None:
        status_candidates = (
            getattr(exc, "status_code", None),
            getattr(exc, "status", None),
            getattr(exc, "http_status", None),
        )

        for candidate in status_candidates:
            if isinstance(candidate, int):
                return candidate

        response = getattr(exc, "response", None)
        if response is not None:
            response_status = getattr(response, "status_code", None)
            if isinstance(response_status, int):
                return response_status

        return None

    @staticmethod
    def _require_non_empty_text(value: str, field_name: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field_name} must not be empty")
        return normalized

    @staticmethod
    def _validate_response_creativity(value: float) -> float:
        try:
            normalized = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("response_creativity must be a number") from exc

        if not 0.0 <= normalized <= 2.0:
            raise ValueError("response_creativity must be between 0.0 and 2.0")
        return normalized

    @staticmethod
    def _validate_rate_limit_configuration(
        rate_limit_max_calls: int | None, rate_limit_window_seconds: float
    ) -> None:
        if rate_limit_max_calls is not None and rate_limit_max_calls <= 0:
            raise ValueError("rate_limit_max_calls must be greater than 0")
        if rate_limit_window_seconds <= 0:
            raise ValueError("rate_limit_window_seconds must be greater than 0")

    @staticmethod
    def _validate_timeout_seconds(timeout_seconds: float) -> float:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than 0")
        return float(timeout_seconds)

    @staticmethod
    def _validate_max_retries(max_retries: int) -> int:
        if max_retries < 0:
            raise ValueError("max_retries must be greater than or equal to 0")
        return max_retries

    def _validate_retry_delay_constants(self) -> None:
        if self.retry_base_delay_seconds <= 0:
            raise ValueError("retry_base_delay_seconds must be greater than 0")
        if self.retry_max_delay_seconds <= 0:
            raise ValueError("retry_max_delay_seconds must be greater than 0")
        if self.retry_base_delay_seconds > self.retry_max_delay_seconds:
            raise ValueError(
                "retry_base_delay_seconds must be less than or equal to retry_max_delay_seconds"
            )

    @staticmethod
    def _is_retryable_error(error: LLMProviderError) -> bool:
        return isinstance(error, (LLMRateLimitError, LLMTemporaryProviderError))
