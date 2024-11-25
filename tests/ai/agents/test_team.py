"""Tests for team agents"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.team import TeamAgent, TeamCoordinator
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
    client.complete = AsyncMock(return_value=AIResponse(
        content="Team task complete",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Team task complete")],
        metadata={"steps": ["step1", "step2"]}
    ))
    return client


@pytest.fixture
def team_config():
    """Fixture for team agent config"""
    return AgentConfig(
        name="team",
        role=AgentRole.MANAGER,
        metadata={"expertise": "team coordination"}
    )


@pytest.mark.asyncio
async def test_team_agent_initialization(mock_ai_client, team_config):
    """Test team agent initialization"""
    agent = TeamAgent(team_config, mock_ai_client)
    assert not agent.is_initialized
    await agent.initialize()
    assert agent.is_initialized
    mock_ai_client.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_team_agent_execute(mock_ai_client, team_config):
    """Test team agent execute method"""
    agent = TeamAgent(team_config, mock_ai_client)
    await agent.initialize()
    
    task = "Team task"
    response = await agent.execute(task)
    
    assert response.content == "Team task complete"
    assert "steps" in response.metadata
    mock_ai_client.complete.assert_called_once()


@pytest.mark.asyncio
async def test_team_coordinator_coordinate(mock_ai_client, team_config):
    """Test team coordinator coordinate method"""
    coordinator = TeamCoordinator(team_config, mock_ai_client)
    await coordinator.initialize()
    
    tasks = ["Task 1", "Task 2"]
    response = await coordinator.coordinate_team(tasks)
    
    assert response.content == "Team task complete"
    assert "steps" in response.metadata
    mock_ai_client.complete.assert_called_once()


@pytest.mark.asyncio
async def test_team_coordinator_with_context(mock_ai_client, team_config):
    """Test team coordinator with context"""
    coordinator = TeamCoordinator(team_config, mock_ai_client)
    await coordinator.initialize()
    
    tasks = ["Task 1", "Task 2"]
    context = {
        "team_size": 5,
        "deadline": "2024-Q2",
        "priority": "high"
    }
    
    response = await coordinator.coordinate_team(tasks, **context)
    
    assert response.content == "Team task complete"
    assert "steps" in response.metadata
    mock_ai_client.complete.assert_called_once()


@pytest.mark.asyncio
async def test_team_agent_error_handling(mock_ai_client, team_config):
    """Test team agent error handling"""
    agent = TeamAgent(team_config, mock_ai_client)
    await agent.initialize()
    
    mock_ai_client.complete.side_effect = PepperPyError("Team task failed")
    
    with pytest.raises(PepperPyError, match="Team task failed"):
        await agent.execute("Invalid task")


@pytest.mark.asyncio
async def test_team_coordinator_error_handling(mock_ai_client, team_config):
    """Test team coordinator error handling"""
    coordinator = TeamCoordinator(team_config, mock_ai_client)
    await coordinator.initialize()
    
    mock_ai_client.complete.side_effect = PepperPyError("Team coordination failed")
    
    with pytest.raises(PepperPyError, match="Team coordination failed"):
        await coordinator.coordinate_team(["Invalid task"])


@pytest.mark.asyncio
async def test_team_agent_cleanup(mock_ai_client, team_config):
    """Test team agent cleanup"""
    agent = TeamAgent(team_config, mock_ai_client)
    await agent.initialize()
    await agent.cleanup()
    mock_ai_client.cleanup.assert_called_once()


@pytest.mark.asyncio
async def test_team_coordinator_cleanup(mock_ai_client, team_config):
    """Test team coordinator cleanup"""
    coordinator = TeamCoordinator(team_config, mock_ai_client)
    await coordinator.initialize()
    await coordinator.cleanup()
    mock_ai_client.cleanup.assert_called_once() 