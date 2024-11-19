"""Advanced team example"""

import asyncio
from typing import cast

from pepperpy.ai import (
    AgentConfig,
    AgentFactory,
    AIClient,
    AIConfig,
)
from pepperpy.ai.agents.interfaces import (
    ArchitectAgent,
    DeveloperAgent,
    QAAgent,
    ReviewerAgent,
)
from pepperpy.ai.agents.team_types import AgentTeam, TeamConfig, TeamRole
from pepperpy.core.logging import get_logger

console = get_logger(__name__)


async def demonstrate_advanced_team() -> None:
    """Demonstrate advanced team workflow"""
    try:
        await console.info("🤖 Initializing Advanced Development Team...")

        # Create AI configuration
        ai_config = AIConfig(
            model="anthropic/claude-3-sonnet",
            temperature=0.7,
            max_tokens=1000,
        )

        # Create team configuration
        team_config = TeamConfig(
            name="Advanced Development Team",
            roles=[
                TeamRole.ARCHITECT,
                TeamRole.DEVELOPER,
                TeamRole.REVIEWER,
                TeamRole.QA,
            ],
            ai_config=ai_config,
        )

        # Create AI client
        client = AIClient(config=ai_config)

        # Create agent configurations
        architect_config = AgentConfig(
            name="architect",
            role="System Architecture",
            ai_config=ai_config,
        )

        developer_config = AgentConfig(
            name="developer",
            role="Development",
            ai_config=ai_config,
        )

        reviewer_config = AgentConfig(
            name="reviewer",
            role="Code Review",
            ai_config=ai_config,
        )

        qa_config = AgentConfig(
            name="qa",
            role="Quality Assurance",
            ai_config=ai_config,
        )

        # Create agents with proper type casting
        architect = cast(
            ArchitectAgent, AgentFactory.create_agent("architect", client, architect_config)
        )
        developer = cast(
            DeveloperAgent, AgentFactory.create_agent("developer", client, developer_config)
        )
        reviewer = cast(
            ReviewerAgent, AgentFactory.create_agent("reviewer", client, reviewer_config)
        )
        qa = cast(QAAgent, AgentFactory.create_agent("qa", client, qa_config))

        # Create and store team reference
        team = AgentTeam(
            config=team_config,
            agents={
                "architect": architect,
                "developer": developer,
                "reviewer": reviewer,
                "qa": qa,
            },
        )

        # Execute tasks
        architecture_task = "Design a scalable microservices architecture"
        development_task = "Implement core services"
        review_task = "Review implementation"
        qa_task = "Test core services"

        await console.info("Starting team workflow...")

        await console.info("Starting architecture design...")
        architecture_result = await architect.design(architecture_task)
        await console.info("Architecture design completed", result=architecture_result.content)

        await console.info("Starting development...")
        development_result = await developer.implement(development_task)
        await console.info("Development completed", result=development_result.content)

        await console.info("Starting code review...")
        review_result = await reviewer.review(review_task)
        await console.info("Code review completed", result=review_result.content)

        await console.info("Starting QA testing...")
        qa_result = await qa.test(qa_task)
        await console.info("QA testing completed", result=qa_result.content)

        # Use team to coordinate tasks
        await team.coordinate(
            [
                (architect, architecture_task),
                (developer, development_task),
                (reviewer, review_task),
                (qa, qa_task),
            ]
        )

    except Exception as e:
        await console.error("Team workflow failed", error=str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_advanced_team())
