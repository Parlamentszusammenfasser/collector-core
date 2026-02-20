from __future__ import annotations

import asyncio

import pytest

from collector_core.llm_connector import (
    DEFAULT_MODELS,
    RETRY_BASE_DELAY_SECONDS,
    RETRY_JITTER_MAX_SECONDS,
    RETRY_JITTER_MIN_SECONDS,
    LLMAuthenticationError,
    LLMConnector,
    LLMConnectorError,
    LLMProvider,
    LLMProviderError,
    LLMQuotaExceededError,
    LLMRateLimitError,
    LLMTemporaryProviderError,
    RateLimiter,
)

# TODO: Review tests. Only automatically generated tests.


def test_default_model_is_selected_for_provider() -> None:
    connector = LLMConnector(provider=LLMProvider.OPENAI)
    assert connector.model == DEFAULT_MODELS[LLMProvider.OPENAI]


def test_custom_model_overrides_default() -> None:
    connector = LLMConnector(provider="claude", model="anthropic/claude-3-5-sonnet-latest")
    assert connector.model == "anthropic/claude-3-5-sonnet-latest"


def test_invalid_provider_raises() -> None:
    with pytest.raises(ValueError, match="unsupported provider"):
        LLMConnector(provider="unknown")


def test_non_string_provider_raises() -> None:
    with pytest.raises(ValueError, match="provider must be an LLMProvider or non-empty string"):
        LLMConnector(provider=None)  # type: ignore[arg-type]


def test_empty_model_raises() -> None:
    with pytest.raises(ValueError, match="model must not be empty"):
        LLMConnector(provider="openai", model="   ")


def test_invalid_response_creativity_raises() -> None:
    with pytest.raises(ValueError, match="response_creativity must be between 0.0 and 2.0"):
        LLMConnector(provider="openai", response_creativity=2.5)


def test_invalid_rate_limit_max_calls_raises() -> None:
    with pytest.raises(ValueError, match="rate_limit_max_calls must be greater than 0"):
        LLMConnector(provider="openai", rate_limit_max_calls=0)


def test_invalid_rate_limit_window_seconds_raises() -> None:
    with pytest.raises(ValueError, match="rate_limit_window_seconds must be greater than 0"):
        LLMConnector(provider="openai", rate_limit_window_seconds=0)


def test_invalid_timeout_seconds_raises() -> None:
    with pytest.raises(ValueError, match="timeout_seconds must be greater than 0"):
        LLMConnector(provider="openai", timeout_seconds=0)


def test_invalid_max_retries_raises() -> None:
    with pytest.raises(ValueError, match="max_retries must be greater than or equal to 0"):
        LLMConnector(provider="openai", max_retries=-1)


def test_generate_text_calls_litellm_with_expected_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    async def fake_completion(**kwargs: object) -> dict[str, object]:
        captured.update(kwargs)
        return {"choices": [{"message": {"content": "Kurze Antwort"}}]}

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_completion)

    connector = LLMConnector(
        provider="mistral",
        model="mistral/mistral-small-latest",
        response_creativity=0.35,
    )
    result = asyncio.run(
        connector.generate_text(prompt="Bitte fasse zusammen", system_prompt="Systemtext")
    )

    assert result == "Kurze Antwort"
    assert captured["model"] == "mistral/mistral-small-latest"
    assert captured["temperature"] == 0.35
    assert captured["messages"] == [
        {"role": "system", "content": "Systemtext"},
        {"role": "user", "content": "Bitte fasse zusammen"},
    ]


def test_generate_text_extracts_list_content(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_completion(**_: object) -> dict[str, object]:
        return {
            "choices": [
                {
                    "message": {
                        "content": [
                            {"type": "text", "text": "Erster Punkt"},
                            {"type": "tool_use", "name": "noop"},
                            {"type": "text", "text": "Zweiter Punkt"},
                        ]
                    }
                }
            ]
        }

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_completion)

    connector = LLMConnector(provider="openai")
    result = asyncio.run(connector.generate_text("Zusammenfassung?"))
    assert result == "Erster Punkt\nZweiter Punkt"


def test_generate_text_rejects_empty_prompt() -> None:
    connector = LLMConnector(provider="openai")
    with pytest.raises(ValueError, match="prompt must not be empty"):
        asyncio.run(connector.generate_text("   "))


def test_generate_text_rejects_empty_system_prompt() -> None:
    connector = LLMConnector(provider="openai")
    with pytest.raises(ValueError, match="system_prompt must not be empty"):
        asyncio.run(connector.generate_text("Inhalt", system_prompt="   "))


def test_generate_text_raises_for_unparseable_response(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_completion(**_: object) -> dict[str, object]:
        return {"choices": []}

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_completion)

    connector = LLMConnector(provider="bedrock")
    with pytest.raises(LLMConnectorError, match="did not contain choices"):
        asyncio.run(connector.generate_text("test"))


def test_summarize_builds_summary_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_messages: list[dict[str, str]] = []

    async def fake_completion(**kwargs: object) -> dict[str, object]:
        messages = kwargs["messages"]
        assert isinstance(messages, list)
        captured_messages.extend(messages)
        return {"choices": [{"message": {"content": "Kurzfassung"}}]}

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_completion)

    connector = LLMConnector(provider="openai")
    result = asyncio.run(
        connector.summarize(
            text="Das ist ein langer Text über ein Gesetzesvorhaben.",
            max_sentences=3,
            language="Deutsch",
        )
    )

    assert result == "Kurzfassung"
    assert captured_messages[0]["role"] == "system"
    assert "politische und juristische Texte" in captured_messages[0]["content"]
    assert captured_messages[1]["role"] == "user"
    assert "maximal 3 Sätzen" in captured_messages[1]["content"]
    assert "Gesetzesvorhaben." in captured_messages[1]["content"]


def test_summarize_rejects_empty_text() -> None:
    connector = LLMConnector(provider="claude")
    with pytest.raises(ValueError, match="text must not be empty"):
        asyncio.run(connector.summarize("   "))


def test_summarize_rejects_invalid_max_sentences() -> None:
    connector = LLMConnector(provider="claude")
    with pytest.raises(ValueError, match="max_sentences must be greater than 0"):
        asyncio.run(connector.summarize("Ein Text", max_sentences=0))


def test_summarize_rejects_empty_language() -> None:
    connector = LLMConnector(provider="claude")
    with pytest.raises(ValueError, match="language must not be empty"):
        asyncio.run(connector.summarize("Ein Text", language="   "))


def test_rate_limiter_waits_until_window_resets(monkeypatch: pytest.MonkeyPatch) -> None:
    clock = {"now": 0.0}
    sleep_calls: list[float] = []

    def fake_monotonic() -> float:
        return clock["now"]

    async def fake_sleep(delay: float) -> None:
        sleep_calls.append(delay)
        clock["now"] += delay

    monkeypatch.setattr("collector_core.llm_connector.time.monotonic", fake_monotonic)
    monkeypatch.setattr("collector_core.llm_connector.asyncio.sleep", fake_sleep)

    limiter = RateLimiter(max_calls=1, per_seconds=10.0)

    async def run_test() -> None:
        await limiter.acquire_slot()
        await limiter.acquire_slot()

    asyncio.run(run_test())

    assert sleep_calls == [10.0]


def test_generate_text_uses_rate_limiter(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyLimiter:
        def __init__(self) -> None:
            self.call_count = 0

        async def acquire_slot(self) -> None:
            self.call_count += 1

    captured: dict[str, object] = {}

    async def fake_acompletion(**kwargs: object) -> dict[str, object]:
        captured.update(kwargs)
        return {"choices": [{"message": {"content": "Asynchrone Antwort"}}]}

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)

    connector = LLMConnector(
        provider="openai", rate_limit_max_calls=2, rate_limit_window_seconds=60.0
    )
    dummy_limiter = DummyLimiter()
    connector._rate_limiter = dummy_limiter  # type: ignore[assignment]

    result = asyncio.run(connector.generate_text(prompt="Bitte kurz", system_prompt="System"))

    assert result == "Asynchrone Antwort"
    assert dummy_limiter.call_count == 1
    assert captured["model"] == connector.model


def test_generate_text_maps_authentication_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class AuthError(Exception):
        status_code = 401

    async def fake_acompletion(**_: object) -> dict[str, object]:
        raise AuthError("unauthorized")

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)
    connector = LLMConnector(provider="openai")

    with pytest.raises(LLMAuthenticationError):
        asyncio.run(connector.generate_text("test"))


def test_generate_text_maps_quota_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class QuotaError(Exception):
        pass

    async def fake_acompletion(**_: object) -> dict[str, object]:
        raise QuotaError("insufficient_quota: budget exhausted")

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)
    connector = LLMConnector(provider="openai")

    with pytest.raises(LLMQuotaExceededError):
        asyncio.run(connector.generate_text("test"))


def test_generate_text_maps_provider_rate_limit_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class RateLimitError(Exception):
        status_code = 429

    async def fake_acompletion(**_: object) -> dict[str, object]:
        raise RateLimitError("too many requests")

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)
    connector = LLMConnector(provider="openai")

    with pytest.raises(LLMRateLimitError):
        asyncio.run(connector.generate_text("test"))


def test_generate_text_maps_temporary_provider_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class TemporaryError(Exception):
        status_code = 503

    async def fake_acompletion(**_: object) -> dict[str, object]:
        raise TemporaryError("service unavailable")

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)
    connector = LLMConnector(provider="openai")

    with pytest.raises(LLMTemporaryProviderError):
        asyncio.run(connector.generate_text("test"))


def test_generate_text_maps_unknown_provider_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_acompletion(**_: object) -> dict[str, object]:
        raise RuntimeError("something unexpected happened")

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)
    connector = LLMConnector(provider="openai")

    with pytest.raises(LLMProviderError):
        asyncio.run(connector.generate_text("test"))


def test_generate_text_retries_temporary_error(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = {"count": 0}
    sleep_calls: list[float] = []
    jitter_value = 0.4

    class TemporaryError(Exception):
        status_code = 503

    async def fake_sleep(delay: float) -> None:
        sleep_calls.append(delay)

    def fake_uniform(lower: float, upper: float) -> float:
        assert lower == RETRY_JITTER_MIN_SECONDS
        assert upper == RETRY_JITTER_MAX_SECONDS
        return jitter_value

    async def fake_acompletion(**_: object) -> dict[str, object]:
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise TemporaryError("service unavailable")
        return {"choices": [{"message": {"content": "ok"}}]}

    monkeypatch.setattr("collector_core.llm_connector.asyncio.sleep", fake_sleep)
    monkeypatch.setattr("collector_core.llm_connector.random.uniform", fake_uniform)
    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)

    connector = LLMConnector(
        provider="openai",
        rate_limit_max_calls=None,
        max_retries=1,
    )
    result = asyncio.run(connector.generate_text("test"))

    assert result == "ok"
    assert attempts["count"] == 2
    assert sleep_calls == [RETRY_BASE_DELAY_SECONDS + jitter_value]


def test_generate_text_does_not_retry_authentication_error(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = {"count": 0}

    class AuthError(Exception):
        status_code = 401

    async def fake_acompletion(**_: object) -> dict[str, object]:
        attempts["count"] += 1
        raise AuthError("unauthorized")

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)

    connector = LLMConnector(provider="openai", rate_limit_max_calls=None, max_retries=3)
    with pytest.raises(LLMAuthenticationError):
        asyncio.run(connector.generate_text("test"))

    assert attempts["count"] == 1


def test_generate_text_timeout_is_mapped_to_temporary_provider_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_acompletion(**_: object) -> dict[str, object]:
        await asyncio.sleep(0.02)
        return {"choices": [{"message": {"content": "too late"}}]}

    monkeypatch.setattr("collector_core.llm_connector.litellm.acompletion", fake_acompletion)

    connector = LLMConnector(
        provider="openai",
        rate_limit_max_calls=None,
        timeout_seconds=0.001,
        max_retries=0,
    )

    with pytest.raises(LLMTemporaryProviderError, match="timed out"):
        asyncio.run(connector.generate_text("test"))
