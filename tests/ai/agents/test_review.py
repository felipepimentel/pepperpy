"""Tests for review agent"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.review import ReviewAgent
from pepperpy.ai.config.agent import AgentConfig
from pepperpy.ai.roles import AgentRole
from pepperpy.ai.types import AIMessage, AIResponse, MessageRole
from pepperpy.core.exceptions import PepperPyError


@pytest.fixture
def mock_ai_client():
    """Fixture for mock AI client"""
    client = AsyncMock()
    client.is_initialized = False
    client.initialize = AsyncMock()
    client.complete = AsyncMock(
        return_value=AIResponse(
            content="Review complete",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Review complete")],
            metadata={"suggestions": ["Add tests", "Improve docs"]},
        )
    )
    return client


@pytest.fixture
def review_config():
    """Fixture for review agent config"""
    return AgentConfig(
        name="reviewer", role=AgentRole.REVIEWER, metadata={"expertise": "code review"}
    )


@pytest.mark.asyncio
async def test_review_agent_initialization(mock_ai_client, review_config):
    """Test review agent initialization"""
    agent = ReviewAgent(review_config, mock_ai_client)
    assert not agent.is_initialized
    await agent.initialize()
    assert agent.is_initialized
    mock_ai_client.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_review_agent_review(mock_ai_client, review_config):
    """Test review agent review method"""
    agent = ReviewAgent(review_config, mock_ai_client)
    await agent.initialize()

    code = """
    def add(a: int, b: int) -> int:
        return a + b
    """

    expected_prompt = (
        f"As a code reviewer with the role of {review_config.role}, "
        f"please review this code:\n\n{code}\n\n"
        "Focus on:\n"
        "- Code quality\n"
        "- Best practices\n"
        "- Potential issues\n"
        "- Documentation\n"
        "- Test coverage"
    )

    response = await agent.review(code)

    assert response.content == "Review complete"
    assert "suggestions" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_review_agent_with_context(mock_ai_client, review_config):
    """Test review agent with context"""
    agent = ReviewAgent(review_config, mock_ai_client)
    await agent.initialize()

    code = "def test(): pass"
    context = {
        "language": "python",
        "standards": ["PEP 8", "Type hints"],
        "focus": ["security", "performance"],
    }

    expected_prompt = (
        f"As a code reviewer with the role of {review_config.role}, "
        f"please review this code:\n\n{code}\n\n"
        "Focus on:\n"
        "- Code quality\n"
        "- Best practices\n"
        "- Potential issues\n"
        "- Documentation\n"
        "- Test coverage\n\n"
        f"Context:\n{context}"
    )

    mock_ai_client.complete = AsyncMock(
        return_value=AIResponse(
            content="Contextualized review",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Contextualized review")],
            metadata={"context": context, "suggestions": ["Add type hints", "Add docstring"]},
        )
    )

    response = await agent.review(code, **context)

    assert response.content == "Contextualized review"
    assert response.metadata["context"] == context
    assert "suggestions" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_review_agent_error_handling(mock_ai_client, review_config):
    """Test review agent error handling"""
    agent = ReviewAgent(review_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Review failed")

    with pytest.raises(PepperPyError, match="Code review failed"):
        await agent.review("Invalid code")


@pytest.mark.asyncio
async def test_review_agent_not_initialized(mock_ai_client, review_config):
    """Test review agent when not initialized"""
    agent = ReviewAgent(review_config, mock_ai_client)

    with pytest.raises(RuntimeError, match="not initialized"):
        await agent.review("Test code")


@pytest.mark.asyncio
async def test_review_agent_execute(mock_ai_client, review_config):
    """Test review agent execute method"""
    agent = ReviewAgent(review_config, mock_ai_client)
    await agent.initialize()

    code = "def test(): pass"
    response = await agent.execute(code)

    assert response.content == "Review complete"
    assert "suggestions" in response.metadata
    mock_ai_client.complete.assert_called_once()
