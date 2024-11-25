"""Tests for specialized agents"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.specialized import (
    AutomatedTestingAgent,
    CodeReviewAgent,
    DocumentationAgent,
    OptimizationAgent,
    SecurityAgent,
)
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
def specialized_config():
    """Fixture for specialized agent config"""
    return AgentConfig(
        name="specialized", role=AgentRole.DEVELOPER, metadata={"expertise": "code quality"}
    )


@pytest.mark.asyncio
async def test_code_review_agent(mock_ai_client, specialized_config):
    """Test code review agent"""
    agent = CodeReviewAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    code = """
    def add(a, b):
        return a + b
    """

    expected_prompt = (
        f"As a code reviewer with the role of {specialized_config.role}, "
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
async def test_code_review_agent_error_handling(mock_ai_client, specialized_config):
    """Test code review agent error handling"""
    agent = CodeReviewAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Review failed")

    with pytest.raises(PepperPyError, match="Code review failed"):
        await agent.review_code("Invalid code")


@pytest.mark.asyncio
async def test_documentation_agent(mock_ai_client, specialized_config):
    """Test documentation agent"""
    agent = DocumentationAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    code = """
    def calculate_total(items: list[float]) -> float:
        return sum(items)
    """

    expected_prompt = (
        f"As a documentation specialist with the role of {specialized_config.role}, "
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
async def test_documentation_agent_error_handling(mock_ai_client, specialized_config):
    """Test documentation agent error handling"""
    agent = DocumentationAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Documentation failed")

    with pytest.raises(PepperPyError, match="Documentation generation failed"):
        await agent.generate_docs("Invalid code")


@pytest.mark.asyncio
async def test_automated_testing_agent_create_tests(mock_ai_client, specialized_config):
    """Test automated testing agent create tests method"""
    agent = AutomatedTestingAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    code = """
    def validate(data: dict) -> bool:
        pass
    """

    expected_prompt = (
        f"As a testing specialist with the role of {specialized_config.role}, "
        f"please create tests for this code:\n\n{code}\n\n"
        "Include:\n"
        "- Unit tests\n"
        "- Integration tests\n"
        "- Edge cases\n"
        "- Test scenarios"
    )

    response = await agent.create_tests(code)

    assert response.content == "Task complete"
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_automated_testing_agent_with_context(mock_ai_client, specialized_config):
    """Test automated testing agent with context"""
    agent = AutomatedTestingAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    code = "def process_data(data: list) -> dict: ..."
    context = {
        "framework": "pytest",
        "coverage_target": "100%",
        "test_types": ["unit", "integration"],
    }

    expected_prompt = (
        f"As a testing specialist with the role of {specialized_config.role}, "
        f"please create tests for this code:\n\n{code}\n\n"
        "Include:\n"
        "- Unit tests\n"
        "- Integration tests\n"
        "- Edge cases\n"
        "- Test scenarios\n\n"
        f"Context:\n{context}"
    )

    mock_ai_client.complete = AsyncMock(
        return_value=AIResponse(
            content="Tests with context",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Tests with context")],
            metadata={"context": context},
        )
    )

    response = await agent.create_tests(code, **context)

    assert response.content == "Tests with context"
    assert response.metadata["context"] == context
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_automated_testing_agent_error_handling(mock_ai_client, specialized_config):
    """Test automated testing agent error handling"""
    agent = AutomatedTestingAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Test creation failed")

    with pytest.raises(PepperPyError, match="Test creation failed"):
        await agent.create_tests("Invalid code")


@pytest.mark.asyncio
async def test_automated_testing_agent_not_initialized(mock_ai_client, specialized_config):
    """Test automated testing agent when not initialized"""
    agent = AutomatedTestingAgent(specialized_config, mock_ai_client)

    with pytest.raises(RuntimeError, match="not initialized"):
        await agent.create_tests("Test code")


@pytest.mark.asyncio
async def test_automated_testing_agent_execute(mock_ai_client, specialized_config):
    """Test automated testing agent execute method"""
    agent = AutomatedTestingAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    code = "def test_function(): pass"
    response = await agent.execute(code)

    assert response.content == "Task complete"
    mock_ai_client.complete.assert_called_once()


@pytest.mark.asyncio
async def test_optimization_agent_optimize(mock_ai_client, specialized_config):
    """Test optimization agent optimize method"""
    agent = OptimizationAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    code = """
    def process_list(items: list) -> list:
        result = []
        for item in items:
            result.append(item * 2)
        return result
    """

    expected_prompt = (
        f"As an optimization specialist with the role of {specialized_config.role}, "
        f"please optimize this code:\n\n{code}\n\n"
        "Focus on:\n"
        "- Performance improvements\n"
        "- Resource usage\n"
        "- Algorithmic efficiency\n"
        "- Memory optimization"
    )

    response = await agent.optimize_code(code)

    assert response.content == "Task complete"
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_optimization_agent_error_handling(mock_ai_client, specialized_config):
    """Test optimization agent error handling"""
    agent = OptimizationAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Optimization failed")

    with pytest.raises(PepperPyError, match="Code optimization failed"):
        await agent.optimize_code("Invalid code")


@pytest.mark.asyncio
async def test_security_agent(mock_ai_client, specialized_config):
    """Test security agent"""
    agent = SecurityAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    code = """
    def authenticate(password: str) -> bool:
        return password == "secret"
    """

    expected_prompt = (
        f"As a security specialist with the role of {specialized_config.role}, "
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
async def test_security_agent_error_handling(mock_ai_client, specialized_config):
    """Test security agent error handling"""
    agent = SecurityAgent(specialized_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = PepperPyError("Security audit failed")

    with pytest.raises(PepperPyError, match="Security audit failed"):
        await agent.audit_code("Invalid code")


@pytest.mark.asyncio
async def test_specialized_agents_with_context(mock_ai_client, specialized_config):
    """Test specialized agents with context"""
    agents = [
        (CodeReviewAgent, "review_code"),
        (DocumentationAgent, "generate_docs"),
        (AutomatedTestingAgent, "create_tests"),
        (OptimizationAgent, "optimize_code"),
        (SecurityAgent, "audit_code"),
    ]

    context = {"language": "python", "version": "3.9", "framework": "fastapi"}

    for agent_class, method_name in agents:
        agent = agent_class(specialized_config, mock_ai_client)
        await agent.initialize()

        code = "def test(): pass"
        method = getattr(agent, method_name)

        mock_ai_client.complete = AsyncMock(
            return_value=AIResponse(
                content="Task with context",
                messages=[AIMessage(role=MessageRole.ASSISTANT, content="Task with context")],
                metadata={"context": context},
            )
        )

        response = await method(code, **context)

        assert response.content == "Task with context"
        assert response.metadata["context"] == context
        assert mock_ai_client.complete.call_count == 1
        mock_ai_client.complete.reset_mock()
