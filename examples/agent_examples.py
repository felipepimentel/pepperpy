"""Agent examples demonstrating different AI agent capabilities"""

import asyncio
import sys

from pepperpy.ai import (
    AgentConfig,
    AgentFactory,
    AIClient,
    AIConfig,
    ResearchAgent,
)
from pepperpy.core.logging import ConsoleLogHandler, get_logger

# Configure logger with console handler
logger = get_logger(__name__)
logger.add_handler(ConsoleLogHandler(sys.stdout))


async def demonstrate_research_agent() -> None:
    """Demonstrate research agent capabilities"""
    try:
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
            role="Research and Analysis",
            ai_config=ai_config,
        )

        # Create research agent
        agent = AgentFactory.create_agent("researcher", client, agent_config)
        if not isinstance(agent, ResearchAgent):
            raise ValueError("Invalid agent type")

        # Initialize agent
        await agent.initialize()

        # Execute research tasks
        tasks = [
            "Research best practices for microservices architecture",
            "Analyze performance implications of different patterns",
            "Investigate scalability solutions",
        ]

        for task in tasks:
            await logger.info(f"Researching: {task}")
            result = await agent.research(task)
            await logger.info("Research completed", result=result.content)

    except Exception as e:
        await logger.error("Error during research", error=str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_research_agent())
