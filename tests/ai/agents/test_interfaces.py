"""Tests for agent interfaces"""

from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.config.agent import AgentConfig
from pepperpy.ai.interfaces import (
    AIProvider,
    AnalystProtocol,
    BaseAgentProtocol,
    DeveloperProtocol,
    ProjectManagerProtocol,
    QAProtocol,
    ResearcherProtocol,
    ReviewerProtocol,
)
from pepperpy.ai.roles import AgentRole
from pepperpy.ai.types import AIMessage, AIResponse, MessageRole


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
        )
    )
    return client


@pytest.fixture
def base_config():
    """Fixture for base agent config"""
    return AgentConfig(name="test", role=AgentRole.DEVELOPER, metadata={"expertise": "testing"})


class ConcreteBaseAgent:
    """Base class for concrete agent implementations"""

    def __init__(self, config: AgentConfig, client: AIProvider) -> None:
        self.config = config
        self._client = client
        self._initialized = False

    @property
    def name(self) -> str:
        """Get agent name"""
        return self.config.name

    @property
    def role(self) -> str:
        """Get agent role"""
        return str(self.config.role)

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get agent metadata"""
        return self.config.metadata

    async def initialize(self) -> None:
        """Initialize agent"""
        if not self._client.is_initialized:
            await self._client.initialize()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        if self._client.is_initialized:
            await self._client.cleanup()
        self._initialized = False


class ConcreteAgent(ConcreteBaseAgent):
    """Concrete agent implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task"""
        return await self._client.complete(task)


class ConcreteManager(ConcreteBaseAgent, ProjectManagerProtocol):
    """Concrete project manager implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task"""
        return await self._client.complete(task)

    async def coordinate(self, tasks: list[str], **kwargs: Any) -> AIResponse:
        """Coordinate tasks"""
        return await self._client.complete(str(tasks))


class ConcreteAnalyst(ConcreteBaseAgent, AnalystProtocol):
    """Concrete analyst implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task"""
        return await self._client.complete(task)

    async def analyze(self, data: str, **kwargs: Any) -> AIResponse:
        """Analyze data"""
        return await self._client.complete(data)


class ConcreteDeveloper(ConcreteBaseAgent, DeveloperProtocol):
    """Concrete developer implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task"""
        return await self._client.complete(task)

    async def implement(self, task: str, **kwargs: Any) -> AIResponse:
        """Implement task"""
        return await self._client.complete(task)


class ConcreteQA(ConcreteBaseAgent, QAProtocol):
    """Concrete QA implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task"""
        return await self._client.complete(task)

    async def test(self, code: str, **kwargs: Any) -> AIResponse:
        """Test code"""
        return await self._client.complete(code)


class ConcreteResearcher(ConcreteBaseAgent, ResearcherProtocol):
    """Concrete researcher implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task"""
        return await self._client.complete(task)

    async def research(self, topic: str, **kwargs: Any) -> AIResponse:
        """Research topic"""
        return await self._client.complete(topic)


class ConcreteReviewer(ConcreteBaseAgent, ReviewerProtocol):
    """Concrete reviewer implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task"""
        return await self._client.complete(task)

    async def review(self, code: str, **kwargs: Any) -> AIResponse:
        """Review code"""
        return await self._client.complete(code)


@pytest.mark.asyncio
async def test_base_agent_protocol(mock_ai_client, base_config):
    """Test base agent protocol"""
    agent = ConcreteAgent(base_config, mock_ai_client)
    await agent.initialize()

    response = await agent.execute("Test task")
    assert response.content == "Task complete"


@pytest.mark.asyncio
async def test_project_manager_protocol(mock_ai_client, base_config):
    """Test project manager protocol"""
    manager = ConcreteManager(base_config, mock_ai_client)
    await manager.initialize()

    response = await manager.coordinate(["Task 1", "Task 2"])
    assert response.content == "Task complete"


@pytest.mark.asyncio
async def test_analyst_protocol(mock_ai_client, base_config):
    """Test analyst protocol"""
    analyst = ConcreteAnalyst(base_config, mock_ai_client)
    await analyst.initialize()

    response = await analyst.analyze("Test data")
    assert response.content == "Task complete"


@pytest.mark.asyncio
async def test_developer_protocol(mock_ai_client, base_config):
    """Test developer protocol"""
    developer = ConcreteDeveloper(base_config, mock_ai_client)
    await developer.initialize()

    response = await developer.implement("Test task")
    assert response.content == "Task complete"


@pytest.mark.asyncio
async def test_qa_protocol(mock_ai_client, base_config):
    """Test QA protocol"""
    qa = ConcreteQA(base_config, mock_ai_client)
    await qa.initialize()

    response = await qa.test("Test code")
    assert response.content == "Task complete"


@pytest.mark.asyncio
async def test_researcher_protocol(mock_ai_client, base_config):
    """Test researcher protocol"""
    researcher = ConcreteResearcher(base_config, mock_ai_client)
    await researcher.initialize()

    response = await researcher.research("Test topic")
    assert response.content == "Task complete"


@pytest.mark.asyncio
async def test_reviewer_protocol(mock_ai_client, base_config):
    """Test reviewer protocol"""
    reviewer = ConcreteReviewer(base_config, mock_ai_client)
    await reviewer.initialize()

    response = await reviewer.review("Test code")
    assert response.content == "Task complete"


class TestAIProvider:
    """Test AI provider implementation"""

    def test_provider_protocol(self, mock_ai_client):
        """Test AI provider protocol"""
        assert isinstance(mock_ai_client, AIProvider)
        assert hasattr(mock_ai_client, "is_initialized")
        assert hasattr(mock_ai_client, "initialize")
        assert hasattr(mock_ai_client, "cleanup")
        assert hasattr(mock_ai_client, "complete")


class TestBaseAgent:
    """Test base agent implementation"""

    def test_base_agent_protocol(self, mock_ai_client, base_config):
        """Test base agent protocol"""
        agent = ConcreteAgent(base_config, mock_ai_client)
        assert isinstance(agent, BaseAgentProtocol)
        assert hasattr(agent, "name")
        assert hasattr(agent, "role")
        assert hasattr(agent, "metadata")
        assert hasattr(agent, "execute")
        assert hasattr(agent, "initialize")
        assert hasattr(agent, "cleanup")


class TestProjectManager:
    """Test project manager implementation"""

    def test_project_manager_protocol(self, mock_ai_client, base_config):
        """Test project manager protocol"""

        class ProjectManager(ConcreteAgent, ProjectManagerProtocol):
            async def coordinate(self, tasks: list[str], **kwargs: Any) -> AIResponse:
                return await self._client.complete(str(tasks))

        manager = ProjectManager(base_config, mock_ai_client)
        assert isinstance(manager, ProjectManagerProtocol)
        assert hasattr(manager, "coordinate")


class TestAnalyst:
    """Test analyst implementation"""

    def test_analyst_protocol(self, mock_ai_client, base_config):
        """Test analyst protocol"""

        class Analyst(ConcreteAgent, AnalystProtocol):
            async def analyze(self, data: str, **kwargs: Any) -> AIResponse:
                return await self._client.complete(data)

        analyst = Analyst(base_config, mock_ai_client)
        assert isinstance(analyst, AnalystProtocol)
        assert hasattr(analyst, "analyze")


class TestDeveloper:
    """Test developer implementation"""

    def test_developer_protocol(self, mock_ai_client, base_config):
        """Test developer protocol"""

        class Developer(ConcreteAgent, DeveloperProtocol):
            async def implement(self, task: str, **kwargs: Any) -> AIResponse:
                return await self._client.complete(task)

        developer = Developer(base_config, mock_ai_client)
        assert isinstance(developer, DeveloperProtocol)
        assert hasattr(developer, "implement")


class TestQA:
    """Test QA implementation"""

    def test_qa_protocol(self, mock_ai_client, base_config):
        """Test QA protocol"""

        class QA(ConcreteAgent, QAProtocol):
            async def test(self, code: str, **kwargs: Any) -> AIResponse:
                return await self._client.complete(code)

        qa = QA(base_config, mock_ai_client)
        assert isinstance(qa, QAProtocol)
        assert hasattr(qa, "test")


class TestResearcher:
    """Test researcher implementation"""

    def test_researcher_protocol(self, mock_ai_client, base_config):
        """Test researcher protocol"""

        class Researcher(ConcreteAgent, ResearcherProtocol):
            async def research(self, topic: str, **kwargs: Any) -> AIResponse:
                return await self._client.complete(topic)

        researcher = Researcher(base_config, mock_ai_client)
        assert isinstance(researcher, ResearcherProtocol)
        assert hasattr(researcher, "research")


class TestReviewer:
    """Test reviewer implementation"""

    def test_reviewer_protocol(self, mock_ai_client, base_config):
        """Test reviewer protocol"""

        class Reviewer(ConcreteAgent, ReviewerProtocol):
            async def review(self, code: str, **kwargs: Any) -> AIResponse:
                return await self._client.complete(code)

        reviewer = Reviewer(base_config, mock_ai_client)
        assert isinstance(reviewer, ReviewerProtocol)
        assert hasattr(reviewer, "review")


@pytest.mark.asyncio
async def test_protocol_execution(mock_ai_client, base_config):
    """Test protocol execution"""

    class TestAgent(ConcreteAgent, DeveloperProtocol):
        async def implement(self, task: str, **kwargs: Any) -> AIResponse:
            return await self._client.complete(task)

    agent = TestAgent(base_config, mock_ai_client)
    await agent.initialize()

    response = await agent.implement("Test task")
    assert response.content == "Task complete"
    mock_ai_client.complete.assert_called_once_with("Test task")


@pytest.mark.asyncio
async def test_protocol_error_handling(mock_ai_client, base_config):
    """Test protocol error handling"""

    class TestAgent(ConcreteAgent, DeveloperProtocol):
        async def implement(self, task: str, **kwargs: Any) -> AIResponse:
            return await self._client.complete(task)

    agent = TestAgent(base_config, mock_ai_client)
    await agent.initialize()

    mock_ai_client.complete.side_effect = Exception("Task failed")

    with pytest.raises(Exception, match="Task failed"):
        await agent.implement("Test task")
