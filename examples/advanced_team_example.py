"""Advanced team example demonstrating multi-agent collaboration"""

import asyncio

from pepperpy.ai import AIClient
from pepperpy.ai.agents import AgentConfig, AgentFactory, AgentRole
from pepperpy.ai.types import AIResponse
from pepperpy.console import Console

console = Console()


async def demonstrate_team_collaboration() -> None:
    """Demonstrate team collaboration"""
    try:
        await console.info("🤖 Initializing AI Team...")

        # Create AI client
        client = AIClient()
        await client.initialize()

        try:
            # Create agent configurations
            architect_config = AgentConfig(
                name="architect",
                role=AgentRole.ARCHITECT,
                metadata={
                    "ai_config": client.config.to_dict(),
                    "instructions": "Design scalable and maintainable architecture solutions",
                },
            )

            developer_config = AgentConfig(
                name="developer",
                role=AgentRole.DEVELOPER,
                metadata={
                    "ai_config": client.config.to_dict(),
                    "instructions": "Implement solutions following best practices",
                },
            )

            reviewer_config = AgentConfig(
                name="reviewer",
                role=AgentRole.REVIEWER,
                metadata={
                    "ai_config": client.config.to_dict(),
                    "instructions": "Review code for quality and improvements",
                },
            )

            qa_config = AgentConfig(
                name="qa",
                role=AgentRole.QA,
                metadata={
                    "ai_config": client.config.to_dict(),
                    "instructions": "Ensure quality through comprehensive testing",
                },
            )

            # Create agents using factory
            factory = AgentFactory()
            architect = factory.create_agent(
                client=client,
                config=architect_config,
                role=AgentRole.ARCHITECT,
            )

            developer = factory.create_agent(
                client=client,
                config=developer_config,
                role=AgentRole.DEVELOPER,
            )

            reviewer = factory.create_agent(
                client=client,
                config=reviewer_config,
                role=AgentRole.REVIEWER,
            )

            qa = factory.create_agent(
                client=client,
                config=qa_config,
                role=AgentRole.QA,
            )

            # Demonstrate team collaboration
            await console.info("Starting team collaboration...")

            # Architect designs solution
            design: AIResponse = await architect.execute(
                "Design a scalable microservices architecture"
            )
            await console.info("Architect's Design:", content=design.content)

            # Developer implements solution
            implementation: AIResponse = await developer.execute(
                f"Implement this design: {design.content}"
            )
            await console.info("Developer's Implementation:", content=implementation.content)

            # Reviewer reviews code
            review: AIResponse = await reviewer.execute(
                f"Review this code: {implementation.content}"
            )
            await console.info("Reviewer's Feedback:", content=review.content)

            # QA tests implementation
            test_results: AIResponse = await qa.execute(
                f"Test this implementation: {implementation.content}"
            )
            await console.info("QA Test Results:", content=test_results.content)

        finally:
            await client.cleanup()

    except Exception as e:
        await console.error("Team collaboration failed", str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_team_collaboration())
