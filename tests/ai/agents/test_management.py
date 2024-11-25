"""Tests for management agents"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.agents.management import (
    ComplianceAgent,
    DevOpsAgent,
    ProjectManagerAgent,
    QualityEngineerAgent,
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
    client.cleanup = AsyncMock()
    client.complete = AsyncMock(
        return_value=AIResponse(
            content="Task complete",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Task complete")],
            metadata={"steps": ["step1", "step2"]},
        )
    )
    return client


@pytest.fixture
def management_config():
    """Fixture for management agent config"""
    return AgentConfig(
        name="manager", role=AgentRole.MANAGER, metadata={"expertise": "project management"}
    )


@pytest.mark.asyncio
async def test_project_manager_coordinate_list(mock_ai_client, management_config):
    """Test project manager coordinate with task list"""
    agent = ProjectManagerAgent(management_config, mock_ai_client)
    await agent.initialize()

    tasks = ["Task 1", "Task 2", "Task 3"]
    tasks_str = "\n".join(f"- {task}" for task in tasks)

    expected_prompt = (
        f"As a project manager with the role of {management_config.role}, "
        f"please coordinate these tasks:\n\n{tasks_str}\n\n"
        "Provide:\n"
        "- Task dependencies\n"
        "- Resource assignments\n"
        "- Timeline coordination\n"
        "- Communication plan"
    )

    response = await agent.coordinate(tasks)

    assert response.content == "Task complete"
    assert "steps" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_project_manager_coordinate_string(mock_ai_client, management_config):
    """Test project manager coordinate with task string"""
    agent = ProjectManagerAgent(management_config, mock_ai_client)
    await agent.initialize()

    task = "Complex project task"

    expected_prompt = (
        f"As a project manager with the role of {management_config.role}, "
        f"please coordinate these tasks:\n\n{task}\n\n"
        "Provide:\n"
        "- Task dependencies\n"
        "- Resource assignments\n"
        "- Timeline coordination\n"
        "- Communication plan"
    )

    response = await agent.coordinate(task)

    assert response.content == "Task complete"
    assert "steps" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_quality_engineer_assess_quality(mock_ai_client, management_config):
    """Test quality engineer assess quality"""
    agent = QualityEngineerAgent(management_config, mock_ai_client)
    await agent.initialize()

    project = "Web application project"

    expected_prompt = (
        f"As a quality engineer with the role of {management_config.role}, "
        f"please assess the quality of:\n\n{project}\n\n"
        "Include:\n"
        "- Quality metrics\n"
        "- Compliance assessment\n"
        "- Areas for improvement\n"
        "- Recommendations"
    )

    response = await agent.assess_quality(project)

    assert response.content == "Task complete"
    assert "steps" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_devops_plan_deployment(mock_ai_client, management_config):
    """Test DevOps plan deployment"""
    agent = DevOpsAgent(management_config, mock_ai_client)
    await agent.initialize()

    project = "Microservices application"

    expected_prompt = (
        f"As a DevOps engineer with the role of {management_config.role}, "
        f"please create a deployment plan for:\n\n{project}\n\n"
        "Include:\n"
        "- Infrastructure requirements\n"
        "- Deployment steps\n"
        "- Monitoring setup\n"
        "- Rollback procedures"
    )

    response = await agent.plan_deployment(project)

    assert response.content == "Task complete"
    assert "steps" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_compliance_check(mock_ai_client, management_config):
    """Test compliance check"""
    agent = ComplianceAgent(management_config, mock_ai_client)
    await agent.initialize()

    task = "GDPR compliance review"

    expected_prompt = (
        f"As a compliance officer with the role of {management_config.role}, "
        f"please check compliance for:\n\n{task}\n\n"
        "Include:\n"
        "- Regulatory requirements\n"
        "- Policy compliance\n"
        "- Risk assessment\n"
        "- Recommendations\n"
        "- Documentation needs"
    )

    response = await agent.check(task)

    assert response.content == "Task complete"
    assert "steps" in response.metadata
    mock_ai_client.complete.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_management_agents_with_context(mock_ai_client, management_config):
    """Test management agents with context"""
    agents = [
        (ProjectManagerAgent, "coordinate"),
        (QualityEngineerAgent, "assess_quality"),
        (DevOpsAgent, "plan_deployment"),
        (ComplianceAgent, "check"),
    ]

    context = {"environment": "production", "team_size": 10, "deadline": "2024-Q2"}

    for agent_class, method_name in agents:
        agent = agent_class(management_config, mock_ai_client)
        await agent.initialize()

        task = "Test task"
        method = getattr(agent, method_name)

        mock_ai_client.complete = AsyncMock(
            return_value=AIResponse(
                content="Task with context",
                messages=[AIMessage(role=MessageRole.ASSISTANT, content="Task with context")],
                metadata={"context": context, "steps": ["step1", "step2"]},
            )
        )

        response = await method(task, **context)

        assert response.content == "Task with context"
        assert response.metadata["context"] == context
        assert "steps" in response.metadata
        assert mock_ai_client.complete.call_count == 1
        mock_ai_client.complete.reset_mock()


@pytest.mark.asyncio
async def test_management_agents_error_handling(mock_ai_client, management_config):
    """Test management agents error handling"""
    agents = [
        (ProjectManagerAgent, "coordinate", "Project coordination failed"),
        (QualityEngineerAgent, "assess_quality", "Quality assessment failed"),
        (DevOpsAgent, "plan_deployment", "Deployment planning failed"),
        (ComplianceAgent, "check", "Compliance check failed"),
    ]

    for agent_class, method_name, error_msg in agents:
        agent = agent_class(management_config, mock_ai_client)
        await agent.initialize()

        mock_ai_client.complete.side_effect = PepperPyError("Task failed")

        method = getattr(agent, method_name)
        with pytest.raises(PepperPyError, match=error_msg):
            await method("Invalid task")

        mock_ai_client.complete.reset_mock()
        mock_ai_client.complete.side_effect = None


@pytest.mark.asyncio
async def test_management_agents_not_initialized(mock_ai_client, management_config):
    """Test management agents when not initialized"""
    agents = [
        (ProjectManagerAgent, "coordinate"),
        (QualityEngineerAgent, "assess_quality"),
        (DevOpsAgent, "plan_deployment"),
        (ComplianceAgent, "check"),
    ]

    for agent_class, method_name in agents:
        agent = agent_class(management_config, mock_ai_client)
        method = getattr(agent, method_name)

        with pytest.raises(RuntimeError, match="not initialized"):
            await method("Test task")
