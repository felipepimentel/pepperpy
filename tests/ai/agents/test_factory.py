"""Tests for agent factory"""

from pepperpy.ai.agents.config import AgentConfig
from pepperpy.ai.agents.factory import AgentFactory


def test_create_code_review_agent():
    """Test creating code review agent"""
    config = AgentConfig(name="code-review")
    agent = AgentFactory.create_agent("code-review", config)
    assert agent is not None


def test_create_documentation_agent():
    """Test creating documentation agent"""
    config = AgentConfig(name="documentation")
    agent = AgentFactory.create_agent("documentation", config)
    assert agent is not None


def test_create_testing_agent():
    """Test creating testing agent"""
    config = AgentConfig(name="testing")
    agent = AgentFactory.create_agent("testing", config)
    assert agent is not None
