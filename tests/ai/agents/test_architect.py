"""Tests for architect agent"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.architect import ArchitectAgent
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
            content="Architecture design complete",
            messages=[
                AIMessage(role=MessageRole.ASSISTANT, content="Architecture design complete")
            ],
        )
    )
    return client


@pytest.fixture
def architect_config():
    """Fixture for architect agent config"""
    return AgentConfig(
        name="architect", role=AgentRole.ARCHITECT, metadata={"expertise": "system architecture"}
    )


@pytest.mark.asyncio
async def test_architect_agent_initialization(mock_ai_client, architect_config):
    """Test architect agent initialization"""
    agent = ArchitectAgent(architect_config, mock_ai_client)
    assert not agent.is_initialized
    await agent.initialize()
    assert agent.is_initialized
    mock_ai_client.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_architect_agent_design(mock_ai_client, architect_config):
    """Test architect agent design method"""
    agent = ArchitectAgent(architect_config, mock_ai_client)
    await agent.initialize()

    requirements = """
    System requirements:
    - User authentication
    - Data storage
    - API endpoints
    - Real-time updates
    """

    expected_prompt = (
        f"As a system architect with the role of {architect_config.role}, "
        f"please design an architecture for:\n\n{requirements}\n\n"
        "Include:\n"
        "- System components\n"
        "- Component interactions\n"
        "- Data flow\n"
        "- Technology stack\n"
        "- Scalability considerations"
    )

    response = await agent.design_architecture(requirements)

    assert response.content == "Architecture design complete"
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_architect_agent_with_constraints(mock_ai_client, architect_config):
    """Test architect agent with constraints"""
    agent = ArchitectAgent(architect_config, mock_ai_client)
    await agent.initialize()

    requirements = "Build a microservices architecture"
    constraints = {
        "budget": "limited",
        "scalability": "high",
        "tech_stack": ["Python", "Docker", "Kubernetes"],
    }

    expected_prompt = (
        f"As a system architect with the role of {architect_config.role}, "
        f"please design an architecture for:\n\n{requirements}\n\n"
        "Include:\n"
        "- System components\n"
        "- Component interactions\n"
        "- Data flow\n"
        "- Technology stack\n"
        "- Scalability considerations\n\n"
        f"Constraints:\n{constraints}"
    )

    mock_ai_client.complete = AsyncMock(
        return_value=AIResponse(
            content="Constrained design",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Constrained design")],
            metadata={"constraints": constraints},
        )
    )

    response = await agent.design_architecture(requirements, constraints=constraints)

    assert response.content == "Constrained design"
    assert response.metadata["constraints"] == constraints
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_architect_agent_error_handling(mock_ai_client, architect_config):
    """Test architect agent error handling"""
    agent = ArchitectAgent(architect_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Design failed")

    with pytest.raises(PepperPyError, match="Design failed"):
        await agent.design_architecture("Invalid requirements")


@pytest.mark.asyncio
async def test_architect_agent_not_initialized(mock_ai_client, architect_config):
    """Test architect agent when not initialized"""
    agent = ArchitectAgent(architect_config, mock_ai_client)

    with pytest.raises(RuntimeError, match="not initialized"):
        await agent.design_architecture("Test requirements")


@pytest.mark.asyncio
async def test_architect_agent_execute(mock_ai_client, architect_config):
    """Test architect agent execute method"""
    agent = ArchitectAgent(architect_config, mock_ai_client)
    await agent.initialize()

    task = "Design a scalable web application"
    response = await agent.execute(task)

    assert response.content == "Architecture design complete"
    mock_ai_client.complete.assert_called_once()
