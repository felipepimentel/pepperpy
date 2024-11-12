"""Tests for AI module"""

from typing import AsyncIterator

import pytest

from pepperpy.ai.exceptions import AIError
from pepperpy.ai.module import AIModule
from pepperpy.ai.providers.base import BaseLLMProvider
from pepperpy.ai.types import LLMResponse, Message


class MockProvider(BaseLLMProvider):
    """Mock LLM provider for testing"""

    async def initialize(self) -> None:
        """Initialize mock provider"""
        pass

    async def cleanup(self) -> None:
        """Cleanup mock provider"""
        pass

    async def generate(self, messages: list[Message]) -> LLMResponse:
        """Generate mock response"""
        return LLMResponse(
            content="Mock response",
            model="mock-model",
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        )

    async def stream(self, messages: list[Message]) -> AsyncIterator[LLMResponse]:
        """Stream mock responses"""
        yield LLMResponse(
            content="Mock stream",
            model="mock-model",
            usage={"prompt_tokens": 5, "completion_tokens": 10, "total_tokens": 15},
        )


@pytest.mark.asyncio
async def test_module_initialization():
    """Test AI module initialization"""
    module = AIModule()
    await module.initialize()
    assert module._initialized

    # Cleanup
    await module.cleanup()


@pytest.mark.asyncio
async def test_module_response():
    """Test AI module response generation"""
    module = AIModule()
    await module.initialize()

    response = await module.generate(
        [
            Message(
                role="user",
                content="Test message",
                usage={"prompt_tokens": 5, "completion_tokens": 10, "total_tokens": 15},
            )
        ]
    )

    assert isinstance(response, LLMResponse)
    assert response.content
    assert response.model

    # Cleanup
    await module.cleanup()


@pytest.mark.asyncio
async def test_module_error_handling():
    """Test AI module error handling"""
    module = AIModule()

    with pytest.raises(AIError):
        await module.generate(
            [
                Message(
                    role="user",
                    content="Test message",
                    usage={"prompt_tokens": 5, "completion_tokens": 10, "total_tokens": 15},
                )
            ]
        )


@pytest.mark.asyncio
async def test_module_context_manager():
    """Test AI module context manager"""
    async with AIModule() as module:
        response = await module.generate(
            [
                Message(
                    role="user",
                    content="Test message",
                    usage={"prompt_tokens": 5, "completion_tokens": 10, "total_tokens": 15},
                )
            ]
        )
        assert isinstance(response, LLMResponse)
