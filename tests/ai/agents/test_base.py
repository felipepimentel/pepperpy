"""Tests for base agent"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.base import BaseAgent
from pepperpy.ai.types import AIMessage, AIResponse, MessageRole


@pytest.fixture
def mock_agent():
    """Fixture for mock agent"""
    class MockAgent(BaseAgent):
        async def execute(self, task: str, **kwargs) -> AIResponse:
            self._ensure_initialized()
            return await self._client.complete(task)
            
    return MockAgent

@pytest.fixture
def mock_ai_client():
    """Fixture for mock AI client"""
    client = AsyncMock()
    client.is_initialized = False
    client.initialize = AsyncMock()
    client.cleanup = AsyncMock()
    client.complete = AsyncMock(return_value=AIResponse(
        content="Test complete",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Test complete")],
        metadata={}
    ))
    return client

# Test cases here...
    