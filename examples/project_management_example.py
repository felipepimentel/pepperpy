"""Project management example"""

import asyncio
from typing import cast

from pepperpy.ai import (
    AgentConfig,
    AgentFactory,
    AIClient,
    AIConfig,
)
from pepperpy.ai.agents.interfaces import ProjectManagerAgent, QAAgent
from pepperpy.core.logging import get_logger

console = get_logger(__name__)


async def demonstrate_project_management() -> None:
    """Demonstrate project management workflow"""
    try:
        await console.info("🤖 Initializing Project Management Team...")

        # Create AI configuration
        ai_config = AIConfig(
            model="anthropic/claude-3-sonnet",
            temperature=0.7,
            max_tokens=1000,
        )

        # Create AI client
        client = AIClient(config=ai_config)

        # Create agent configurations
        manager_config = AgentConfig(
            name="manager",
            role="Project Management",
            ai_config=ai_config,
        )

        qa_config = AgentConfig(
            name="qa",
            role="Quality Assurance",
            ai_config=ai_config,
        )

        # Create agents with proper type casting
        manager = cast(ProjectManagerAgent,
            AgentFactory.create_agent("project_manager", client, manager_config))
        qa = cast(QAAgent,
            AgentFactory.create_agent("qa", client, qa_config))

        # Execute tasks
        planning_task = "Create project plan for new feature development"
        qa_task = "Define quality assurance strategy"

        await console.info("Starting project management workflow...")

        await console.info("Starting project planning...")
        planning_result = await manager.plan(planning_task)
        await console.info("Project planning completed", result=planning_result.content)

        await console.info("Starting QA testing...")
        qa_result = await qa.test(qa_task)
        await console.info("QA strategy defined", result=qa_result.content)

    except Exception as e:
        await console.error("Project management workflow failed", error=str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_project_management())
