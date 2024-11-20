"""Agent examples demonstrating different AI agent capabilities"""

import asyncio
import sys
from typing import cast

from pepperpy.ai import (
    AgentConfig,
    AgentFactory,
    AgentRole,
    AIClient,
    AIConfig,
)
from pepperpy.ai.agents.interfaces import ResearchAgent
from pepperpy.core.logging import get_logger

logger = get_logger(__name__)


async def demonstrate_research_agent() -> None:
    """Demonstrate research agent capabilities"""
    try:
        # Use print for immediate feedback
        print("🤖 Initializing Research Agent...")
        await logger.info("🤖 Initializing Research Agent...")

        # Create AI configuration
        ai_config = AIConfig(
            model="anthropic/claude-3-sonnet",
            temperature=0.7,
            max_tokens=1000,
        )

        # Create AI client
        client = AIClient(ai_config)
        await client.initialize()

        # Create agent configuration
        agent_config = AgentConfig(
            name="researcher",
            role=AgentRole.RESEARCHER,
            metadata={"ai_config": ai_config.to_dict()},
        )

        # Create research agent with proper type casting
        agent = cast(ResearchAgent, AgentFactory.create_agent("researcher", client, agent_config))

        # Initialize agent
        await agent.initialize()

        # Execute research tasks
        tasks = [
            "Research best practices for microservices architecture",
            "Analyze performance implications of different patterns",
            "Investigate scalability solutions",
        ]

        for task in tasks:
            print(f"\n📚 Researching: {task}")
            await logger.info(f"Researching: {task}")

            result = await agent.research(task)

            print("\n✅ Research completed:")
            print(f"{result.content}\n")
            await logger.info("Research completed", result=result.content)

    except Exception as e:
        print(f"\n❌ Error during research: {e}", file=sys.stderr)
        await logger.error("Error during research", error=str(e))
        raise


if __name__ == "__main__":
    try:
        asyncio.run(demonstrate_research_agent())
    except KeyboardInterrupt:
        print("\n\n⚠️ Research interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}", file=sys.stderr)
