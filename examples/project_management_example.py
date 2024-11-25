"""Project management example"""

import asyncio
from typing import cast

from dotenv import load_dotenv  # Importing dotenv

from pepperpy.ai import AIClient, AIConfig
from pepperpy.ai.agents import AgentFactory, ProjectManager, QAAgent
from pepperpy.ai.config.agent import AgentConfig
from pepperpy.ai.roles import AgentRole
from pepperpy.core.logging import get_logger

load_dotenv()  # Loading environment variables

logger = get_logger(__name__)


async def demonstrate_project_management() -> None:
    """Demonstrate project management workflow"""
    client = None
    manager = None
    qa = None

    try:
        await logger.info("🤖 Initializing Project Management...")

        # Create AI configuration
        ai_config = AIConfig.model_validate({"name": "project-management"})

        # Create AI client with the obtained configuration
        client = AIClient(config=ai_config)
        await client.initialize()

        # Create agent configurations
        manager_config = AgentConfig(
            name="manager", role=AgentRole.MANAGER, metadata={"ai_config": client.config.dict()}
        )

        qa_config = AgentConfig(
            name="qa", role=AgentRole.QA, metadata={"ai_config": client.config.dict()}
        )

        # Create agents using factory with proper type casting
        manager = cast(ProjectManager, AgentFactory.create_agent("manager", config=manager_config))
        qa = cast(QAAgent, AgentFactory.create_agent("qa", config=qa_config))

        # Initialize agents
        await manager.initialize()
        await qa.initialize()

        # Execute tasks
        planning_task = "Create project plan for microservices migration"
        testing_task = "Design test strategy for migration"

        await logger.info("Starting planning...")
        planning_result = await manager.plan(planning_task)
        await logger.info("Planning completed", result=planning_result.content)

        await logger.info("Starting test planning...")
        testing_result = await qa.plan_tests(testing_task)
        await logger.info("Test planning completed", result=testing_result.content)

    except Exception as e:
        await logger.error("Project management failed", error=str(e))
        raise  # Re-raise the exception after logging

    finally:
        # Cleanup resources in reverse order
        if qa:
            await qa.cleanup()
        if manager:
            await manager.cleanup()
        if client:
            await client.cleanup()


if __name__ == "__main__":
    asyncio.run(demonstrate_project_management())
