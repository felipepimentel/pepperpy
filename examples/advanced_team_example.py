"""Advanced team example"""

import asyncio
import sys
from typing import Any, Tuple, cast

from pepperpy.ai import (
    AgentConfig,
    AgentFactory,
    AgentRole,
    AIClient,
    AIConfig,
    ArchitectAgent,
    DevelopmentAgent,
    QAAgent,
    ReviewerAgent,
)
from pepperpy.ai.agents import AgentTeam
from pepperpy.ai.agents.team_types import TeamConfig, TeamRole
from pepperpy.core.logging import get_logger

logger = get_logger(__name__)


async def execute_agent_task(agent: Any, task: str) -> str:
    """Execute individual agent task"""
    print(f"\n👉 {agent.config.name.title()} working on: {task}")
    
    try:
        if isinstance(agent, ArchitectAgent):
            result = await agent.design(task)
        elif isinstance(agent, DevelopmentAgent):
            result = await agent.implement(task)
        elif isinstance(agent, ReviewerAgent):
            result = await agent.review(task)
        elif isinstance(agent, QAAgent):
            result = await agent.plan_tests(task)
        else:
            raise ValueError(f"Unknown agent type: {type(agent)}")
        
        return result.content
    except Exception as e:
        print(f"\n⚠️ Error in {agent.config.name}: {str(e)}")
        return f"Error: {str(e)}"


async def demonstrate_team_workflow() -> None:
    """Demonstrate advanced team workflow"""
    client = None
    try:
        print("\n🤖 Initializing Development Team...")
        await logger.info("Initializing Development Team...")

        # Create AI configuration
        ai_config = AIConfig(
            model="anthropic/claude-3-sonnet",
            temperature=0.7,
            max_tokens=1000,
        )

        print("📋 Creating team configuration...")
        # Create team configuration
        team_config = TeamConfig(
            name="development_team",
            roles=[
                TeamRole.ARCHITECT,
                TeamRole.DEVELOPER,
                TeamRole.REVIEWER,
                TeamRole.QA,
            ],
        )

        # Create AI client
        print("🔌 Initializing AI client...")
        client = AIClient(ai_config)
        await client.initialize()

        # Create agent configurations with specific instructions
        print("⚙️ Creating agent configurations...")
        agent_configs = {
            "architect": AgentConfig(
                name="architect",
                role=AgentRole.ARCHITECT,
                metadata={
                    "ai_config": ai_config.to_dict(),
                    "instructions": "Design scalable and maintainable architecture solutions"
                }
            ),
            "developer": AgentConfig(
                name="developer",
                role=AgentRole.DEVELOPER,
                metadata={
                    "ai_config": ai_config.to_dict(),
                    "instructions": "Implement solutions following best practices"
                }
            ),
            "reviewer": AgentConfig(
                name="reviewer",
                role=AgentRole.REVIEWER,
                metadata={
                    "ai_config": ai_config.to_dict(),
                    "instructions": "Review code for quality and improvements"
                }
            ),
            "qa": AgentConfig(
                name="qa",
                role=AgentRole.QA,
                metadata={
                    "ai_config": ai_config.to_dict(),
                    "instructions": "Ensure quality through comprehensive testing"
                }
            )
        }

        # Create agents with proper type casting
        print("🤖 Creating specialized agents...")
        agents = {
            "architect": cast(
                ArchitectAgent,
                AgentFactory.create_agent("architect", client, agent_configs["architect"])
            ),
            "developer": cast(
                DevelopmentAgent,
                AgentFactory.create_agent("developer", client, agent_configs["developer"])
            ),
            "reviewer": cast(
                ReviewerAgent,
                AgentFactory.create_agent("reviewer", client, agent_configs["reviewer"])
            ),
            "qa": cast(
                QAAgent,
                AgentFactory.create_agent("qa", client, agent_configs["qa"])
            )
        }

        # Initialize agents
        print("🔄 Initializing agents...")
        await asyncio.gather(
            *[agent.initialize() for agent in agents.values()]
        )

        # Create team
        print("👥 Creating development team...")
        team = AgentTeam(config=team_config, ai_client=client)
        for name, agent in agents.items():
            team.add_agent(name, agent)

        # Define tasks
        tasks: list[Tuple[Any, str]] = [
            (agents["architect"], "Design a scalable microservices architecture for an e-commerce platform"),
            (agents["developer"], "Implement the core services including user auth, product catalog, and order processing"),
            (agents["reviewer"], "Review the implementation focusing on security and scalability"),
            (agents["qa"], "Design a comprehensive test strategy for the microservices"),
        ]

        print("\n📝 Starting team tasks...")
        for agent, task in tasks:
            print(f"\n🔍 {agent.config.name.title()}'s Task: {task}")

        # Execute tasks sequentially to avoid recursion
        results = []
        for agent, task in tasks:
            result = await execute_agent_task(agent, task)
            results.append(result)

        # Combine results
        final_output = "\n\n".join([
            f"=== {agent.config.name.title()} Output ===\n{result}"
            for (agent, _), result in zip(tasks, results)
        ])

        print("\n✅ Team execution completed!")
        print("\nFinal Results:")
        print("=" * 80)
        print(final_output)
        print("=" * 80)

    except Exception as e:
        error_msg = f"Team workflow failed: {str(e)}"
        print(f"\n❌ {error_msg}", file=sys.stderr)
        await logger.error(error_msg)
        raise

    finally:
        if client:
            print("\n🧹 Cleaning up resources...")
            await client.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(demonstrate_team_workflow())
    except KeyboardInterrupt:
        print("\n\n⚠️ Team workflow interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}", file=sys.stderr)
