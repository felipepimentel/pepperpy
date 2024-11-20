"""Complete development example"""

import asyncio
from typing import cast

from pepperpy.ai import (
    AgentConfig,
    AgentFactory,
    AgentRole,
    AIClient,
    AIConfig,
)
from pepperpy.ai.agents.interfaces import AnalystAgent, ResearchAgent
from pepperpy.core.logging import get_logger

logger = get_logger(__name__)


async def demonstrate_complete_development() -> None:
    """Demonstrate complete development workflow"""
    try:
        await logger.info("🤖 Initializing Development Team...")

        # Create AI configuration
        ai_config = AIConfig(
            model="anthropic/claude-3-sonnet",
            temperature=0.7,
            max_tokens=1000,
        )

        # Create AI client
        client = AIClient(ai_config)
        await client.initialize()

        # Create agent configurations
        researcher_config = AgentConfig(
            name="researcher",
            role=AgentRole.RESEARCHER,
            metadata={"ai_config": ai_config.to_dict()},
        )

        analyst_config = AgentConfig(
            name="analyst", role=AgentRole.ANALYST, metadata={"ai_config": ai_config.to_dict()}
        )

        # Create agents using factory with proper type casting
        researcher = cast(
            ResearchAgent, AgentFactory.create_agent("researcher", client, researcher_config)
        )
        analyst = cast(AnalystAgent, AgentFactory.create_agent("analyst", client, analyst_config))

        # Initialize agents
        await researcher.initialize()
        await analyst.initialize()

        # Execute tasks
        research_task = "Research best practices for microservices architecture"
        analysis_task = "Analyze performance implications of different patterns"

        await logger.info("Starting research...")
        research_result = await researcher.research(research_task)
        await logger.info("Research completed", result=research_result.content)

        await logger.info("Starting analysis...")
        analysis_result = await analyst.analyze(analysis_task)
        await logger.info("Analysis completed", result=analysis_result.content)

    except Exception as e:
        await logger.error("Development process failed", error=str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_complete_development())
