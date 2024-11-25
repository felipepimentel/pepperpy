"""Tests for development agent"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.development import DevelopmentAgent
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
    client.complete = AsyncMock(return_value=AIResponse(
        content="Implementation complete",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Implementation complete")]
    ))
    return client


@pytest.fixture
def dev_config():
    """Fixture for development agent config"""
    return AgentConfig(
        name="developer",
        role=AgentRole.DEVELOPER,
        metadata={"expertise": "python"}
    )


@pytest.mark.asyncio
async def test_development_agent_implement(mock_ai_client, dev_config):
    """Test development agent implement method"""
    agent = DevelopmentAgent(dev_config, mock_ai_client)
    await agent.initialize()
    
    task = """
    Create a function that:
    - Takes two numbers as input
    - Returns their sum
    - Includes type hints
    - Has docstring
    - Includes error handling
    """
    
    response = await agent.implement(task)
    
    assert response.content == "Implementation complete"
    mock_ai_client.complete.assert_called_once_with(
        f"As a development agent with the role of {AgentRole.DEVELOPER}, "
        f"please implement:\n\n{task}\n\n"
        "Include:\n"
        "- Code implementation\n"
        "- Tests\n"
        "- Documentation\n"
        "- Error handling"
    )


@pytest.mark.asyncio
async def test_development_agent_with_context(mock_ai_client, dev_config):
    """Test development agent with context"""
    agent = DevelopmentAgent(dev_config, mock_ai_client)
    await agent.initialize()
    
    context = {
        "language": "python",
        "framework": "fastapi",
        "requirements": ["async", "type-safe"]
    }
    
    mock_ai_client.complete = AsyncMock(return_value=AIResponse(
        content="Implementation with context",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Implementation with context")],
        metadata=context
    ))
    
    response = await agent.implement("Implement endpoint", context=context)
    
    assert response.content == "Implementation with context"
    assert response.metadata == context


@pytest.mark.asyncio
async def test_development_agent_error_handling(mock_ai_client, dev_config):
    """Test development agent error handling"""
    agent = DevelopmentAgent(dev_config, mock_ai_client)
    await agent.initialize()
    
    mock_ai_client.complete.side_effect = PepperPyError("Implementation failed")
    
    with pytest.raises(PepperPyError, match="Implementation failed"):
        await agent.implement("Invalid task")


@pytest.mark.asyncio
async def test_development_agent_with_code_review(mock_ai_client, dev_config):
    """Test development agent with code review"""
    agent = DevelopmentAgent(dev_config, mock_ai_client)
    await agent.initialize()
    
    code = """
    def add(a: int, b: int) -> int:
        return a + b
    """
    
    mock_ai_client.complete = AsyncMock(return_value=AIResponse(
        content="Code review complete",
        messages=[
            AIMessage(role=MessageRole.USER, content=f"Review code:\n{code}"),
            AIMessage(role=MessageRole.ASSISTANT, content="Code review complete")
        ],
        metadata={"suggestions": ["Add docstring", "Add error handling"]}
    ))
    
    response = await agent.implement(f"Review code:\n{code}")
    
    assert response.content == "Code review complete"
    assert "suggestions" in response.metadata


@pytest.mark.asyncio
async def test_development_agent_with_test_generation(mock_ai_client, dev_config):
    """Test development agent test generation"""
    agent = DevelopmentAgent(dev_config, mock_ai_client)
    await agent.initialize()
    
    code = """
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    """
    
    mock_ai_client.complete = AsyncMock(return_value=AIResponse(
        content="Test cases generated",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Test cases generated")],
        metadata={
            "test_cases": [
                "test_valid_division",
                "test_division_by_zero",
                "test_float_division"
            ]
        }
    ))
    
    response = await agent.implement(f"Generate tests for:\n{code}")
    
    assert response.content == "Test cases generated"
    assert "test_cases" in response.metadata 