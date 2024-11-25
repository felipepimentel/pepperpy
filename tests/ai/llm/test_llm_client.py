"""Tests for LLM client module"""

from typing import Any, AsyncGenerator, Dict, List

import pytest

from pepperpy.ai.llm.client import LLMClient
from pepperpy.ai.llm.config import LLMConfig, LLMProvider
from pepperpy.ai.llm.exceptions import LLMError
from pepperpy.ai.llm.types import AIResponse, Role
from pepperpy.ai.providers.config import ProviderConfig
from pepperpy.ai.providers.types import ProviderType


class MockLLMProvider:
    """Mock LLM provider for testing"""

    def __init__(self) -> None:
        """Initialize provider"""
        self._config = ProviderConfig(
            provider=ProviderType.OPENAI, api_key="test-key", model="test-model", metadata={}
        )
        self._initialized = False
        self._responses: List[str] = []

    @property
    def config(self) -> ProviderConfig:
        """Get provider configuration"""
        return self._config

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize provider"""
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup provider"""
        self._initialized = False

    async def complete(self, prompt: str, **kwargs: Dict[str, Any]) -> AIResponse:
        """Complete prompt"""
        if not self._initialized:
            raise RuntimeError("Provider not initialized")

        if not prompt:
            raise LLMError("Empty prompt")

        return AIResponse(
            content="Test response",
            role=Role.ASSISTANT,
            model=self.config.model,
            usage={"total_tokens": 10},
        )

    async def stream(
        self, prompt: str, **kwargs: Dict[str, Any]
    ) -> AsyncGenerator[AIResponse, None]:
        """Stream responses"""
        if not self._initialized:
            raise RuntimeError("Provider not initialized")

        if not prompt:
            raise LLMError("Empty prompt")

        for response in self._responses:
            yield AIResponse(
                content=response,
                role=Role.ASSISTANT,
                model=self.config.model,
                usage={"total_tokens": 2},
            )


@pytest.fixture
def llm_config():
    """Fixture for LLM config"""
    return LLMConfig(
        name="test-llm",
        provider=LLMProvider.OPENAI,
        model="test-model",
        temperature=0.7,
        max_tokens=100,
        metadata={"environment": "test"},
    )


@pytest.fixture
def llm_client(llm_config):
    """Fixture for LLM client"""
    return LLMClient(config=llm_config)


# Rest of the test file remains the same...
