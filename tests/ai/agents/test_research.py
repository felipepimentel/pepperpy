"""Tests for research agent"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.research import ResearchAgent
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
        content="Research complete",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Research complete")],
        metadata={"findings": ["finding1", "finding2"]}
    ))
    return client


@pytest.fixture
def research_config():
    """Fixture for research agent config"""
    return AgentConfig(
        name="researcher",
        role=AgentRole.RESEARCHER,
        metadata={"expertise": "research"}
    )


@pytest.mark.asyncio
async def test_research_agent_initialization(mock_ai_client, research_config):
    """Test research agent initialization"""
    agent = ResearchAgent(research_config, mock_ai_client)
    assert not agent.is_initialized
    await agent.initialize()
    assert agent.is_initialized
    mock_ai_client.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_research_agent_research(mock_ai_client, research_config):
    """Test research agent research method"""
    agent = ResearchAgent(research_config, mock_ai_client)
    await agent.initialize()
    
    topic = "AI testing patterns"
    parameters = {"depth": "detailed"}
    sources = [{"url": "example.com", "title": "Testing Guide"}]
    
    expected_prompt = (
        "Research topic: AI testing patterns\n"
        "Provide comprehensive analysis including:\n"
        "- Current state\n"
        "- Key developments\n"
        "- Future implications\n"
        "Parameters: {'depth': 'detailed'}\n"
        "Sources: [{'url': 'example.com', 'title': 'Testing Guide'}]"
    )
    
    response = await agent.research(
        topic,
        parameters=parameters,
        sources=sources
    )
    
    assert response.content == "Research complete"
    assert "findings" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_research_agent_citations(mock_ai_client, research_config):
    """Test research agent with citations"""
    agent = ResearchAgent(research_config, mock_ai_client)
    await agent.initialize()
    
    citations = [
        "[1] Author et al. (2023)",
        "[2] Another Author (2024)"
    ]
    
    mock_ai_client.complete = AsyncMock(return_value=AIResponse(
        content="Research with citations",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Research with citations")],
        metadata={"citations": citations}
    ))
    
    response = await agent.research("Machine learning", include_citations=True)
    
    assert response.content == "Research with citations"
    assert "citations" in response.metadata
    assert len(response.metadata["citations"]) == 2


@pytest.mark.asyncio
async def test_research_agent_summary(mock_ai_client, research_config):
    """Test research agent with summary"""
    agent = ResearchAgent(research_config, mock_ai_client)
    await agent.initialize()
    
    summary = {
        "key_findings": ["Finding 1", "Finding 2"],
        "recommendations": ["Rec 1", "Rec 2"],
        "limitations": ["Limit 1"]
    }
    
    mock_ai_client.complete = AsyncMock(return_value=AIResponse(
        content="Research with summary",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Research with summary")],
        metadata={"summary": summary}
    ))
    
    response = await agent.research("Data science", include_summary=True)
    
    assert response.content == "Research with summary"
    assert "summary" in response.metadata
    assert len(response.metadata["summary"]["key_findings"]) == 2


@pytest.mark.asyncio
async def test_research_agent_error_handling(mock_ai_client, research_config):
    """Test research agent error handling"""
    agent = ResearchAgent(research_config, mock_ai_client)
    await agent.initialize()
    
    mock_ai_client.complete.side_effect = PepperPyError("Research failed")
    
    with pytest.raises(PepperPyError, match="Research failed"):
        await agent.research("Test topic")


@pytest.mark.asyncio
async def test_research_agent_not_initialized(mock_ai_client, research_config):
    """Test research agent when not initialized"""
    agent = ResearchAgent(research_config, mock_ai_client)
    
    with pytest.raises(RuntimeError, match="not initialized"):
        await agent.research("Test topic")


@pytest.mark.asyncio
async def test_research_agent_cleanup(mock_ai_client, research_config):
    """Test research agent cleanup"""
    agent = ResearchAgent(research_config, mock_ai_client)
    await agent.initialize()
    mock_ai_client.is_initialized = True  # Set client as initialized
    await agent.cleanup()
    
    assert not agent.is_initialized
    mock_ai_client.cleanup.assert_called_once()


@pytest.mark.asyncio
async def test_research_agent_execute(mock_ai_client, research_config):
    """Test research agent execute method"""
    agent = ResearchAgent(research_config, mock_ai_client)
    await agent.initialize()
    
    task = "Research this topic"
    response = await agent.execute(task)
    
    assert response.content == "Research complete"
    assert "findings" in response.metadata