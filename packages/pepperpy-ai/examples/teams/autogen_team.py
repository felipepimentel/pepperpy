"""Example demonstrating AutoGen team functionality"""

import asyncio

from pepperpy_ai import AIClient, AIConfig
from pepperpy_ai.config.agent import AgentConfig
from pepperpy_ai.roles import AgentRole
from pepperpy_ai.teams.config import TeamConfig, TeamFramework
from pepperpy_ai.teams.manager import TeamManager


async def demonstrate_autogen() -> None:
    """Demonstrate autogen workflow"""
    try:
        print("🤖 Initializing AutoGen Team...")

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
                    name="autogen_team",
                    framework=TeamFramework.AUTOGEN,
                    metadata={
                        "project": "pepperpy",
                        "domain": "AI development",
                    },
                )

                # Create agent configurations
                agent_configs = [
                    AgentConfig(
                        name="planner",
                        role=AgentRole.PLANNER,
                        metadata={"specialty": "task planning"},
                    ),
                    AgentConfig(
                        name="executor",
                        role=AgentRole.EXECUTOR,
                        metadata={"specialty": "task execution"},
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
                        "Plan project structure",
                        "Implement core features",
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
        print("AutoGen workflow failed:", str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_autogen())
