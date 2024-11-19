"""Complete development example"""

import asyncio
from typing import cast

from pepperpy.ai import (
    AgentConfig,
    AgentFactory,
    AIClient,
    AIConfig,
)
from pepperpy.ai.agents.interfaces import AnalystAgent, ResearcherAgent
from pepperpy.core.logging import get_logger

console = get_logger(__name__)


async def demonstrate_complete_development() -> None:
    """Demonstrate complete development workflow"""
    try:
        await console.info("🤖 Initializing Development Team...")

        # Create AI configuration
        ai_config = AIConfig(
            model="anthropic/claude-3-sonnet",
            temperature=0.7,
            max_tokens=1000,
        )

        # Create AI client
        client = AIClient(config=ai_config)

        # Create agent configurations
        researcher_config = AgentConfig(
            name="researcher",
            role="Research and Analysis",
            ai_config=ai_config,
        )

        analyst_config = AgentConfig(
            name="analyst",
            role="Data Analysis",
            ai_config=ai_config,
        )

        # Create agents using factory with proper type casting
        researcher = cast(ResearcherAgent,
            AgentFactory.create_agent("researcher", client, researcher_config))
        analyst = cast(AnalystAgent,
            AgentFactory.create_agent("analyst", client, analyst_config))

        # Execute tasks
        research_task = "Research best practices for microservices architecture"
        analysis_task = "Analyze performance implications of different patterns"

        await console.info("Starting research...")
        research_result = await researcher.research(research_task)
        await console.info("Research completed", result=research_result.content)

        await console.info("Starting analysis...")
        analysis_result = await analyst.analyze(analysis_task)
        await console.info("Analysis completed", result=analysis_result.content)

    except Exception as e:
        await console.error("Development process failed", error=str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_complete_development()) 