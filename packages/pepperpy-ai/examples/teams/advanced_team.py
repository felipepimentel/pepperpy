"""Example demonstrating advanced team functionality"""

import asyncio

from pepperpy_ai import AIClient, AIConfig
from pepperpy_ai.config.agent import AgentConfig
from pepperpy_ai.roles import AgentRole
from pepperpy_ai.teams.config import TeamConfig, TeamFramework
from pepperpy_ai.teams.manager import TeamManager


async def demonstrate_advanced_team() -> None:
    """Demonstrate advanced team workflow"""
    try:
        print("🤖 Initializing Advanced Team...")

        # Create AI configuration and client
        config = AIConfig.model_validate({})
        client = AIClient(config=config)
        await client.initialize()

        try:
            # Create team manager
            team_manager = TeamManager()
            await team_manager.initialize()

            try:
                # Create team configuration
                team_config = TeamConfig(
                    name="development_team",
                    framework=TeamFramework.AUTOGEN,
                    metadata={
                        "project": "pepperpy",
                        "domain": "AI development",
                    },
                )

                # Create agent configurations
                agent_configs = [
                    AgentConfig(
                        name="architect",
                        role=AgentRole.DEVELOPER,
                        metadata={"specialty": "architecture"},
                    ),
                    AgentConfig(
                        name="researcher",
                        role=AgentRole.RESEARCHER,
                        metadata={"specialty": "technical research"},
                    ),
                    AgentConfig(
                        name="reviewer",
                        role=AgentRole.REVIEWER,
                        metadata={"specialty": "code review"},
                    ),
                ]

                # Create team
                team = await team_manager.create_team(
                    config=team_config,
                    agent_configs=agent_configs,
                    ai_client=client,
                )

                try:
                    # Execute team tasks
                    print("Starting team tasks...")

                    tasks = [
                        "Design system architecture",
                        "Research best practices",
                        "Review implementation",
                    ]

                    for task in tasks:
                        print(f"Executing task: {task}")
                        result = await team.execute_task(task)
                        print("Task completed:", result.content)

                finally:
                    await team.cleanup()

            finally:
                await team_manager.cleanup()

        finally:
            await client.cleanup()

    except Exception as e:
        print("Team workflow failed:", str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_advanced_team())
