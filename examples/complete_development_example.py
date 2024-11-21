"""Complete development example"""

import asyncio

from pepperpy.ai import (
    AIClient,
    AIConfig,
)
from pepperpy.ai.agents.development import DevelopmentAgent
from pepperpy.ai.config.agent import AgentConfig
from pepperpy.ai.roles import AgentRole
from pepperpy.ai.types import AIResponse
from pepperpy.console import Console

console = Console()


async def demonstrate_complete_development() -> None:
    """Demonstrate complete development workflow"""
    try:
        await console.info("🤖 Initializing Development Team...")

        # Create AI configuration and client
        ai_config = AIConfig.get_default()
        client = AIClient(config=ai_config)
        await client.initialize()

        try:
            # Create agent configurations
            researcher_config = AgentConfig(
                name="researcher",
                role=AgentRole.RESEARCHER,
                metadata={
                    "ai_config": client.config.dict(),
                    "instructions": "Research and gather information on technical topics",
                },
            )

            analyst_config = AgentConfig(
                name="analyst",
                role=AgentRole.ANALYST,
                metadata={
                    "ai_config": client.config.dict(),
                    "instructions": "Analyze technical information and provide insights",
                },
            )

            # Create agents using DevelopmentAgent
            researcher = DevelopmentAgent(
                client=client,
                config=researcher_config,
            )
            await researcher.initialize()

            analyst = DevelopmentAgent(
                client=client,
                config=analyst_config,
            )
            await analyst.initialize()

            try:
                # Demonstrate team collaboration
                await console.info("Starting research...")
                research_task = "Research best practices for microservices architecture"
                research_result: AIResponse = await researcher.implement(research_task)
                await console.info("Research completed:", content=research_result.content)

                await console.info("Starting analysis...")
                analysis_task = (
                    f"Analyze these microservices best practices: {research_result.content}"
                )
                analysis_result: AIResponse = await analyst.implement(analysis_task)
                await console.info("Analysis completed:", content=analysis_result.content)

            finally:
                # Cleanup agents
                await researcher.cleanup()
                await analyst.cleanup()

        finally:
            await client.cleanup()

    except Exception as e:
        await console.error("Development process failed", str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_complete_development())
