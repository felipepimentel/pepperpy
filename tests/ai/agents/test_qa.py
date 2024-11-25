"""Tests for QA agent"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.qa import QAAgent
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
    client.cleanup = AsyncMock()
    client.complete = AsyncMock(
        return_value=AIResponse(
            content="Test complete",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Test complete")],
            metadata={"test_cases": ["case1", "case2"]},
        )
    )
    return client


@pytest.fixture
def qa_config():
    """Fixture for QA agent config"""
    return AgentConfig(name="qa", role=AgentRole.QA, metadata={"expertise": "testing"})


@pytest.mark.asyncio
async def test_qa_agent_initialization(mock_ai_client, qa_config):
    """Test QA agent initialization"""
    agent = QAAgent(qa_config, mock_ai_client)
    assert not agent.is_initialized
    await agent.initialize()
    assert agent.is_initialized
    mock_ai_client.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_qa_agent_test_code(mock_ai_client, qa_config):
    """Test QA agent test code method"""
    agent = QAAgent(qa_config, mock_ai_client)
    await agent.initialize()

    code = """
    def add(a: int, b: int) -> int:
        return a + b
    """

    expected_prompt = (
        f"As a QA engineer with the role of {qa_config.role}, "
        f"please test this code:\n\n{code}\n\n"
        "Include:\n"
        "- Test cases\n"
        "- Edge cases\n"
        "- Error scenarios\n"
        "- Test coverage"
    )

    response = await agent.test_code(code)

    assert response.content == "Test complete"
    assert "test_cases" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_qa_agent_test_with_context(mock_ai_client, qa_config):
    """Test QA agent test with context"""
    agent = QAAgent(qa_config, mock_ai_client)
    await agent.initialize()

    code = "def add(a, b): return a + b"
    context = {"language": "python", "framework": "pytest"}

    expected_prompt = (
        f"As a QA engineer with the role of {qa_config.role}, "
        f"please test this code:\n\n{code}\n\n"
        "Include:\n"
        "- Test cases\n"
        "- Edge cases\n"
        "- Error scenarios\n"
        "- Test coverage\n\n"
        "Context:\n{'language': 'python', 'framework': 'pytest'}"
    )

    response = await agent.test_code(code, **context)

    assert response.content == "Test complete"
    assert "test_cases" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_qa_agent_error_handling(mock_ai_client, qa_config):
    """Test QA agent error handling"""
    agent = QAAgent(qa_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Testing failed")

    with pytest.raises(PepperPyError, match="Testing failed"):
        await agent.test_code("def broken(): pass")


@pytest.mark.asyncio
async def test_qa_agent_not_initialized(mock_ai_client, qa_config):
    """Test QA agent when not initialized"""
    agent = QAAgent(qa_config, mock_ai_client)

    with pytest.raises(RuntimeError, match="not initialized"):
        await agent.test_code("def test(): pass")


@pytest.mark.asyncio
async def test_qa_agent_cleanup(mock_ai_client, qa_config):
    """Test QA agent cleanup"""
    agent = QAAgent(qa_config, mock_ai_client)
    await agent.initialize()
    await agent.cleanup()

    assert not agent.is_initialized
    mock_ai_client.cleanup.assert_called_once()


@pytest.mark.asyncio
async def test_qa_agent_execute(mock_ai_client, qa_config):
    """Test QA agent execute method"""
    agent = QAAgent(qa_config, mock_ai_client)
    await agent.initialize()

    code = "def test(): pass"
    response = await agent.execute(code)

    assert response.content == "Test complete"
    assert "test_cases" in response.metadata
