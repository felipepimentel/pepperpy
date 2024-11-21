"""Autogen examples"""

import asyncio

from pepperpy.ai import AIClient, AIConfig
from pepperpy.ai.config.agent import AgentConfig
from pepperpy.ai.roles import AgentRole
from pepperpy.ai.teams.config import TeamConfig, TeamFramework
from pepperpy.ai.teams.manager import TeamManager
from pepperpy.console import Console

console = Console()


async def demonstrate_autogen() -> None:
    """Demonstrate autogen workflow"""
    try:
        console.info("🤖 Initializing Autogen Team...")

        # Create AI configuration and client
        ai_config = AIConfig(
            provider="openai",
            api_key="your-api-key",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=2048,
        )
        client = AIClient(config=ai_config)
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
                        name="architect",
                        role=AgentRole.DEVELOPER,
                        metadata={"specialty": "architecture"},
                    ),
                    AgentConfig(
                        name="researcher",
                        role=AgentRole.RESEARCHER,
                        metadata={"specialty": "technical research"},
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
                    console.info("Starting team tasks...")

                    tasks = [
                        "Design system architecture",
                        "Research best practices",
                    ]

                    for task in tasks:
                        console.info(f"Executing task: {task}")
                        result = await team.execute_task(task)
                        console.info("Task completed:", content=result.content)

                finally:
                    await team.cleanup()

            finally:
                await team_manager.cleanup()

        finally:
            await client.cleanup()

    except Exception as e:
        console.error("Autogen workflow failed", str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_autogen())
