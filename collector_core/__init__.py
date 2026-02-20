"""
collector_core - Core library for collecting parliamentary data
"""

from .llm_connector import LLMConnector, LLMConnectorError, LLMProvider, LLMProviderError

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "LLMConnector",
    "LLMProvider",
    "LLMConnectorError",
    "LLMProviderError",
]
