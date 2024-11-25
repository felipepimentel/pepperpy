"""Tests for researcher agent"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.researcher import ResearcherAgent
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
            content="Research complete",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Research complete")],
            metadata={"sources": ["source1", "source2"]},
        )
    )
    return client


@pytest.fixture
def researcher_config():
    """Fixture for researcher agent config"""
    return AgentConfig(
        name="researcher", role=AgentRole.RESEARCHER, metadata={"expertise": "technical research"}
    )


@pytest.mark.asyncio
async def test_researcher_agent_initialization(mock_ai_client, researcher_config):
    """Test researcher agent initialization"""
    agent = ResearcherAgent(researcher_config, mock_ai_client)
    assert not agent.is_initialized
    await agent.initialize()
    assert agent.is_initialized
    mock_ai_client.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_researcher_agent_research(mock_ai_client, researcher_config):
    """Test researcher agent research method"""
    agent = ResearcherAgent(researcher_config, mock_ai_client)
    await agent.initialize()

    topic = "Modern microservices architecture patterns"

    expected_prompt = (
        f"As a technical researcher with the role of {researcher_config.role}, "
        f"please research:\n\n{topic}\n\n"
        "Include:\n"
        "- Key findings\n"
        "- Best practices\n"
        "- Current trends\n"
        "- Practical examples\n"
        "- References"
    )

    response = await agent.research(topic)

    assert response.content == "Research complete"
    assert "sources" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_researcher_agent_with_kwargs(mock_ai_client, researcher_config):
    """Test researcher agent with additional kwargs"""
    agent = ResearcherAgent(researcher_config, mock_ai_client)
    await agent.initialize()

    topic = "Containerization strategies"
    kwargs = {
        "focus_areas": ["security", "scalability"],
        "tech_stack": ["Docker", "Kubernetes"],
        "depth": "advanced",
    }

    expected_prompt = (
        f"As a technical researcher with the role of {researcher_config.role}, "
        f"please research:\n\n{topic}\n\n"
        "Include:\n"
        "- Key findings\n"
        "- Best practices\n"
        "- Current trends\n"
        "- Practical examples\n"
        "- References\n\n"
        f"Context:\n{kwargs}"
    )

    mock_ai_client.complete = AsyncMock(
        return_value=AIResponse(
            content="Contextualized research",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Contextualized research")],
            metadata={"context": kwargs, "sources": ["source1", "source2"]},
        )
    )

    response = await agent.research(topic, **kwargs)

    assert response.content == "Contextualized research"
    assert response.metadata["context"] == kwargs
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_researcher_agent_error_handling(mock_ai_client, researcher_config):
    """Test researcher agent error handling"""
    agent = ResearcherAgent(researcher_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Research failed")

    with pytest.raises(PepperPyError, match="Research failed"):
        await agent.research("Invalid topic")


@pytest.mark.asyncio
async def test_researcher_agent_not_initialized(mock_ai_client, researcher_config):
    """Test researcher agent when not initialized"""
    agent = ResearcherAgent(researcher_config, mock_ai_client)

    with pytest.raises(RuntimeError, match="not initialized"):
        await agent.research("Test topic")


@pytest.mark.asyncio
async def test_researcher_agent_execute(mock_ai_client, researcher_config):
    """Test researcher agent execute method"""
    agent = ResearcherAgent(researcher_config, mock_ai_client)
    await agent.initialize()

    task = "Research emerging AI technologies"
    response = await agent.execute(task)

    assert response.content == "Research complete"
    assert "sources" in response.metadata
    mock_ai_client.complete.assert_called_once()
