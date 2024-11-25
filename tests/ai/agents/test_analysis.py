"""Tests for analysis agent"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.analysis import AnalysisAgent, DataAnalystAgent
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
            content="Analysis complete",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Analysis complete")],
            metadata={"findings": ["finding1", "finding2"]},
        )
    )
    return client


@pytest.fixture
def analysis_config():
    """Fixture for analysis agent config"""
    return AgentConfig(
        name="analyst", role=AgentRole.ANALYST, metadata={"expertise": "data analysis"}
    )


@pytest.mark.asyncio
async def test_analysis_agent_initialization(mock_ai_client, analysis_config):
    """Test analysis agent initialization"""
    agent = AnalysisAgent(analysis_config, mock_ai_client)
    assert not agent.is_initialized
    await agent.initialize()
    assert agent.is_initialized
    mock_ai_client.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_analysis_agent_analyze(mock_ai_client, analysis_config):
    """Test analysis agent analyze method"""
    agent = AnalysisAgent(analysis_config, mock_ai_client)
    await agent.initialize()

    data = "Test data for analysis"
    context = {"depth": "detailed"}

    response = await agent.analyze(data, context=context)

    assert response.content == "Analysis complete"
    assert "findings" in response.metadata
    mock_ai_client.complete.assert_called_once()


@pytest.mark.asyncio
async def test_analysis_agent_evaluate(mock_ai_client, analysis_config):
    """Test analysis agent evaluate method"""
    agent = AnalysisAgent(analysis_config, mock_ai_client)
    await agent.initialize()

    results = "Test results"
    confidence = "high"
    context = {"validation": "strict"}

    response = await agent.evaluate(results, confidence=confidence, context=context)

    assert response.content == "Analysis complete"
    assert "findings" in response.metadata
    mock_ai_client.complete.assert_called_once()


@pytest.mark.asyncio
async def test_data_analyst_agent_analyze(mock_ai_client, analysis_config):
    """Test data analyst agent analyze method"""
    agent = DataAnalystAgent(analysis_config, mock_ai_client)
    await agent.initialize()

    data = "Test data"
    context = {"statistical": True}

    response = await agent.analyze(data, **context)

    assert response.content == "Analysis complete"
    assert "findings" in response.metadata
    mock_ai_client.complete.assert_called_once()


@pytest.mark.asyncio
async def test_data_analyst_agent_evaluate(mock_ai_client, analysis_config):
    """Test data analyst agent evaluate method"""
    agent = DataAnalystAgent(analysis_config, mock_ai_client)
    await agent.initialize()

    results = "Test results"
    context = {"confidence": "high"}

    response = await agent.evaluate(results, **context)

    assert response.content == "Analysis complete"
    assert "findings" in response.metadata
    mock_ai_client.complete.assert_called_once()


@pytest.mark.asyncio
async def test_analysis_agent_error_handling(mock_ai_client, analysis_config):
    """Test analysis agent error handling"""
    agent = AnalysisAgent(analysis_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Analysis failed")

    with pytest.raises(PepperPyError, match="Analysis failed"):
        await agent.analyze("Test data")


@pytest.mark.asyncio
async def test_analysis_agent_not_initialized(mock_ai_client, analysis_config):
    """Test analysis agent when not initialized"""
    agent = AnalysisAgent(analysis_config, mock_ai_client)

    with pytest.raises(RuntimeError, match="not initialized"):
        await agent.analyze("Test data")


@pytest.mark.asyncio
async def test_analysis_agent_cleanup(mock_ai_client, analysis_config):
    """Test analysis agent cleanup"""
    agent = AnalysisAgent(analysis_config, mock_ai_client)
    await agent.initialize()
    mock_ai_client.is_initialized = True  # Set client as initialized
    await agent.cleanup()

    # First verify client cleanup was called
    mock_ai_client.cleanup.assert_called_once()

    # Then verify agent state
    assert not agent.is_initialized
