"""
collector_core - Core library for collecting parliamentary data
"""

from .llm_connector import (
    LLMAuthenticationError,
    LLMConnector,
    LLMConnectorError,
    LLMProvider,
    LLMProviderError,
    LLMQuotaExceededError,
    LLMRateLimitError,
    LLMTemporaryProviderError,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "LLMConnector",
    "LLMProvider",
    "LLMConnectorError",
    "LLMProviderError",
    "LLMAuthenticationError",
    "LLMQuotaExceededError",
    "LLMRateLimitError",
    "LLMTemporaryProviderError",
]
