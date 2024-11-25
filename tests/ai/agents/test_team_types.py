"""Tests for team types"""


import pytest

from pepperpy.ai.agents.team_types import (
    TeamConfig,
    TeamContext,
    TeamMember,
    TeamResult,
    TeamRole,
    TeamTask,
)
from pepperpy.ai.roles import AgentRole
from pepperpy.ai.types import AIMessage, AIResponse, MessageRole


def test_team_role_creation():
    """Test team role creation"""
    role = TeamRole(
        name="developer",
        description="Software developer",
        responsibilities=["coding", "testing"]
    )
    
    assert role.name == "developer"
    assert role.description == "Software developer"
    assert role.responsibilities == ["coding", "testing"]


def test_team_member_creation():
    """Test team member creation"""
    role = TeamRole(
        name="developer",
        description="Software developer",
        responsibilities=["coding", "testing"]
    )
    
    member = TeamMember(
        name="Alice",
        role=role,
        agent_role=AgentRole.DEVELOPER,
        expertise=["Python", "Testing"]
    )
    
    assert member.name == "Alice"
    assert member.role == role
    assert member.agent_role == AgentRole.DEVELOPER
    assert member.expertise == ["Python", "Testing"]


def test_team_config_creation():
    """Test team config creation"""
    roles = [
        TeamRole(name="dev", description="Developer", responsibilities=["coding"]),
        TeamRole(name="qa", description="QA Engineer", responsibilities=["testing"])
    ]
    
    members = [
        TeamMember(name="Alice", role=roles[0], agent_role=AgentRole.DEVELOPER, expertise=["Python"]),
        TeamMember(name="Bob", role=roles[1], agent_role=AgentRole.QA, expertise=["Testing"])
    ]
    
    config = TeamConfig(
        name="dev_team",
        description="Development team",
        roles=roles,
        members=members,
        metadata={"project": "test"}
    )
    
    assert config.name == "dev_team"
    assert config.description == "Development team"
    assert config.roles == roles
    assert config.members == members
    assert config.metadata == {"project": "test"}


def test_team_context_creation():
    """Test team context creation"""
    context = TeamContext(
        task_id="task-123",
        team_id="team-456",
        metadata={"priority": "high"},
        state={"progress": 50}
    )
    
    assert context.task_id == "task-123"
    assert context.team_id == "team-456"
    assert context.metadata == {"priority": "high"}
    assert context.state == {"progress": 50}


def test_team_task_creation():
    """Test team task creation"""
    task = TeamTask(
        id="task-123",
        description="Implement feature",
        assignee="Alice",
        dependencies=["task-456"],
        metadata={"priority": "high"},
        context={"deadline": "2024-Q2"}
    )
    
    assert task.id == "task-123"
    assert task.description == "Implement feature"
    assert task.assignee == "Alice"
    assert task.dependencies == ["task-456"]
    assert task.metadata == {"priority": "high"}
    assert task.context == {"deadline": "2024-Q2"}


def test_team_result_creation():
    """Test team result creation"""
    result = TeamResult(
        task_id="task-123",
        status="completed",
        success=True,
        output=AIResponse(
            content="Task completed",
            messages=[AIMessage(role=MessageRole.ASSISTANT, content="Task completed")],
            metadata={"steps": ["step1", "step2"]}
        ),
        metadata={"duration": "2h"},
        errors=[]
    )
    
    assert result.task_id == "task-123"
    assert result.status == "completed"
    assert result.success is True
    assert isinstance(result.output, AIResponse)
    assert result.metadata == {"duration": "2h"}
    assert result.errors == []


def test_team_result_with_errors():
    """Test team result with errors"""
    errors = [
        {"code": "ERR001", "message": "Task failed"},
        {"code": "ERR002", "message": "Timeout"}
    ]
    
    result = TeamResult(
        task_id="task-123",
        status="failed",
        success=False,
        output=None,
        metadata={},
        errors=errors
    )
    
    assert result.task_id == "task-123"
    assert result.status == "failed"
    assert result.success is False
    assert result.output is None
    assert result.errors == errors


def test_team_config_validation():
    """Test team config validation"""
    with pytest.raises(ValueError):
        TeamConfig(
            name="",  # Empty name should raise error
            description="Development team",
            roles=[],
            members=[],
            metadata={}
        )


def test_team_task_validation():
    """Test team task validation"""
    with pytest.raises(ValueError):
        TeamTask(
            id="",  # Empty ID should raise error
            description="Implement feature",
            assignee="Alice",
            dependencies=[],
            metadata={},
            context={}
        )


def test_team_result_validation():
    """Test team result validation"""
    with pytest.raises(ValueError):
        TeamResult(
            task_id="",  # Empty task_id should raise error
            status="completed",
            success=True,
            output=None,
            metadata={},
            errors=[]
        )
    