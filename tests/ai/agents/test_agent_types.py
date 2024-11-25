"""Tests for agent types"""

import pytest

from pepperpy.ai.agents.types import AgentCapability, AgentMetrics, AgentState, AgentStatus


def test_agent_state_creation():
    """Test agent state creation"""
    state = AgentState(
        is_busy=False,
        current_task="test task",
        last_active="2024-01-01",
        metrics={"tasks_completed": 10},
    )

    assert not state.is_busy
    assert state.current_task == "test task"
    assert state.last_active == "2024-01-01"
    assert state.metrics == {"tasks_completed": 10}


def test_agent_state_validation():
    """Test agent state validation"""
    with pytest.raises(ValueError, match="Current task cannot be empty"):
        AgentState(
            is_busy=False,
            current_task="",  # Empty task should raise error
            last_active="2024-01-01",
            metrics={},
        )


def test_agent_state_default_metrics():
    """Test agent state default metrics"""
    state = AgentState(is_busy=True, current_task="test task", last_active="2024-01-01")

    assert state.metrics == {}


def test_agent_status_creation():
    """Test agent status creation"""
    status = AgentStatus(online=True, health_check="passed", last_error=None, uptime="1h")

    assert status.online
    assert status.health_check == "passed"
    assert status.last_error is None
    assert status.uptime == "1h"


def test_agent_status_with_error():
    """Test agent status with error"""
    status = AgentStatus(
        online=False, health_check="failed", last_error="Connection timeout", uptime=None
    )

    assert not status.online
    assert status.health_check == "failed"
    assert status.last_error == "Connection timeout"
    assert status.uptime is None


def test_agent_status_default_values():
    """Test agent status default values"""
    status = AgentStatus(online=True, health_check="passed")

    assert status.last_error is None
    assert status.uptime is None


def test_agent_capability_creation():
    """Test agent capability creation"""
    capability = AgentCapability(
        name="code_review",
        description="Can review code",
        parameters={"languages": ["python", "javascript"]},
        requires_context=True,
    )

    assert capability.name == "code_review"
    assert capability.description == "Can review code"
    assert capability.parameters == {"languages": ["python", "javascript"]}
    assert capability.requires_context


def test_agent_capability_validation():
    """Test agent capability validation"""
    with pytest.raises(ValueError, match="Capability name cannot be empty"):
        AgentCapability(
            name="",  # Empty name should raise error
            description="Can review code",
            parameters={},
            requires_context=True,
        )


def test_agent_capability_default_values():
    """Test agent capability default values"""
    capability = AgentCapability(name="test", description="Test capability")

    assert capability.parameters == {}
    assert not capability.requires_context


def test_agent_metrics_creation():
    """Test agent metrics creation"""
    metrics = AgentMetrics(
        tasks_completed=10, success_rate=0.95, average_response_time=1.5, error_rate=0.05
    )

    assert metrics.tasks_completed == 10
    assert metrics.success_rate == 0.95
    assert metrics.average_response_time == 1.5
    assert metrics.error_rate == 0.05


def test_agent_metrics_validation():
    """Test agent metrics validation"""
    with pytest.raises(ValueError, match="Tasks completed cannot be negative"):
        AgentMetrics(
            tasks_completed=-1,  # Negative value should raise error
            success_rate=0.95,
            average_response_time=1.5,
            error_rate=0.05,
        )


def test_agent_metrics_rate_validation():
    """Test agent metrics rate validation"""
    with pytest.raises(ValueError, match="Success rate must be between 0 and 1"):
        AgentMetrics(
            tasks_completed=10,
            success_rate=1.5,  # Rate > 1.0 should raise error
            average_response_time=1.5,
            error_rate=0.05,
        )


def test_agent_metrics_error_rate_validation():
    """Test agent metrics error rate validation"""
    with pytest.raises(ValueError, match="Error rate must be between 0 and 1"):
        AgentMetrics(
            tasks_completed=10,
            success_rate=0.95,
            average_response_time=1.5,
            error_rate=1.5,  # Rate > 1.0 should raise error
        )


def test_agent_metrics_response_time_validation():
    """Test agent metrics response time validation"""
    with pytest.raises(ValueError, match="Average response time cannot be negative"):
        AgentMetrics(
            tasks_completed=10,
            success_rate=0.95,
            average_response_time=-1.0,  # Negative value should raise error
            error_rate=0.05,
        )


def test_agent_metrics_boundary_values():
    """Test agent metrics boundary values"""
    metrics = AgentMetrics(
        tasks_completed=0,  # Minimum valid value
        success_rate=1.0,  # Maximum valid value
        average_response_time=0.0,  # Minimum valid value
        error_rate=0.0,  # Minimum valid value
    )

    assert metrics.tasks_completed == 0
    assert metrics.success_rate == 1.0
    assert metrics.average_response_time == 0.0
    assert metrics.error_rate == 0.0


def test_agent_metrics_string_representation():
    """Test agent metrics string representation"""
    metrics = AgentMetrics(
        tasks_completed=10, success_rate=0.95, average_response_time=1.5, error_rate=0.05
    )

    expected_str = "AgentMetrics(tasks_completed=10, success_rate=0.95, average_response_time=1.5, error_rate=0.05)"
    assert str(metrics) == expected_str
