"""Tests for additional specialized agents"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.specialized import CodeReviewAgent, DocumentationAgent, SecurityAgent
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
            content="Task complete",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Task complete")],
        )
    )
    return client


@pytest.fixture
def review_config():
    """Fixture for code review agent config"""
    return AgentConfig(
        name="reviewer", role=AgentRole.REVIEWER, metadata={"expertise": "code review"}
    )


@pytest.fixture
def doc_config():
    """Fixture for documentation agent config"""
    return AgentConfig(
        name="documenter", role=AgentRole.DEVELOPER, metadata={"expertise": "documentation"}
    )


@pytest.fixture
def security_config():
    """Fixture for security agent config"""
    return AgentConfig(
        name="security", role=AgentRole.DEVELOPER, metadata={"expertise": "security"}
    )


@pytest.mark.asyncio
async def test_code_review_agent(mock_ai_client, review_config):
    """Test code review agent"""
    agent = CodeReviewAgent(review_config, mock_ai_client)
    await agent.initialize()

    code = """
    def insecure_function(user_input):
        return eval(user_input)
    """

    expected_prompt = (
        f"As a code reviewer with the role of {review_config.role}, "
        f"please review this code:\n\n{code}\n\n"
        "Focus on:\n"
        "- Code quality\n"
        "- Best practices\n"
        "- Potential issues\n"
        "- Suggested improvements"
    )

    response = await agent.review_code(code)

    assert response.content == "Task complete"
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_documentation_agent(mock_ai_client, doc_config):
    """Test documentation agent"""
    agent = DocumentationAgent(doc_config, mock_ai_client)
    await agent.initialize()

    code = """
    def calculate_total(items: list[float]) -> float:
        return sum(items)
    """

    expected_prompt = (
        f"As a documentation specialist with the role of {doc_config.role}, "
        f"please document this code:\n\n{code}\n\n"
        "Include:\n"
        "- Overview\n"
        "- Usage examples\n"
        "- API documentation\n"
        "- Implementation details"
    )

    response = await agent.generate_docs(code)

    assert response.content == "Task complete"
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_security_agent(mock_ai_client, security_config):
    """Test security agent"""
    agent = SecurityAgent(security_config, mock_ai_client)
    await agent.initialize()

    code = """
    def process_user_data(user_input):
        query = f"SELECT * FROM users WHERE id = {user_input}"
        return execute_query(query)
    """

    expected_prompt = (
        f"As a security specialist with the role of {security_config.role}, "
        f"please audit this code:\n\n{code}\n\n"
        "Focus on:\n"
        "- Security vulnerabilities\n"
        "- Best practices\n"
        "- Risk assessment\n"
        "- Security recommendations"
    )

    response = await agent.audit_code(code)

    assert response.content == "Task complete"
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_code_review_agent_error_handling(mock_ai_client, review_config):
    """Test code review agent error handling"""
    agent = CodeReviewAgent(review_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Review failed")

    with pytest.raises(PepperPyError, match="Review failed"):
        await agent.review_code("invalid code")


@pytest.mark.asyncio
async def test_documentation_agent_error_handling(mock_ai_client, doc_config):
    """Test documentation agent error handling"""
    agent = DocumentationAgent(doc_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Documentation failed")

    with pytest.raises(PepperPyError, match="Documentation failed"):
        await agent.generate_docs("invalid code")


@pytest.mark.asyncio
async def test_security_agent_error_handling(mock_ai_client, security_config):
    """Test security agent error handling"""
    agent = SecurityAgent(security_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Security audit failed")

    with pytest.raises(PepperPyError, match="Security audit failed"):
        await agent.audit_code("invalid code")
