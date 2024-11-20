"""AutoGen examples demonstrating multi-agent collaboration"""

import asyncio
from typing import Optional, Union

from pepperpy.ai import AIClient, AIConfig
from pepperpy.ai.autogen.agents import (
    CoderAgent,
    CriticAgent,
    ExecutorAgent,
    PlannerAgent,
)
from pepperpy.ai.autogen.agents.team import AgentTeam, TeamConfig
from pepperpy.ai.types import AIResponse
from pepperpy.console import Console

console = Console()


def get_content(response: Optional[Union[str, AIResponse]]) -> str:
    """Extract content from response"""
    if response is None:
        return ""
    if isinstance(response, AIResponse):
        return response.content
    return response


async def setup_development_team(client: AIClient) -> AgentTeam:
    """Setup a development team with specialized agents"""

    # Criar agentes especializados
    planner = PlannerAgent(
        name="Tech Architect",
        client=client,
        instructions=(
            "You are an expert technical architect focused on planning and system design. "
            "Analyze requirements and create detailed technical specifications."
        ),
    )

    coder = CoderAgent(
        name="Senior Developer",
        client=client,
        instructions=(
            "You are an expert Python developer focused on clean, efficient code. "
            "Implement solutions following best practices and patterns."
        ),
    )

    executor = ExecutorAgent(
        name="Implementation Lead",
        client=client,
        instructions=(
            "You are responsible for implementing solutions and coordinating development efforts. "
            "Focus on practical implementation and integration."
        ),
    )

    critic = CriticAgent(
        name="Code Reviewer",
        client=client,
        instructions=(
            "You are a thorough code reviewer focused on quality and best practices. "
            "Analyze code for potential issues and improvements."
        ),
    )

    # Configurar e retornar o time
    team_config = TeamConfig(
        max_iterations=5,
        timeout=600.0,  # 10 minutes
        parallel_execution=True,
        review_required=True,
    )

    team = AgentTeam(agents=[planner, coder, executor, critic], config=team_config)
    await team.initialize()
    return team


async def demonstrate_code_development() -> None:
    """Demonstrate collaborative code development"""
    try:
        await console.info("🤖 Initializing Development Team...")

        # Criar configuração do AI usando valores padrão do ambiente
        ai_config = AIConfig()

        # Criar cliente AI
        client = AIClient(ai_config)
        await client.initialize()

        try:
            team = await setup_development_team(client)

            # Definir tarefa de desenvolvimento
            task = """
            Create a Python function that implements a custom cache decorator with the following features:
            1. Configurable timeout
            2. Maximum size limit
            3. LRU eviction policy
            4. Thread-safe implementation
            5. Support for async functions
            """

            await console.info(
                "📋 Starting Development Task", title="Task Definition", content=task
            )

            # Executar tarefa com o time
            result = await team.execute_task(task)

            if result.success:
                await console.success(
                    "Development completed",
                    title="🎉 Final Result",
                    content=get_content(result.output),
                )

                # Mostrar passos do desenvolvimento
                await console.info("📝 Development Steps:")
                for i, step in enumerate(result.steps, 1):
                    content = step["content"]
                    metadata = step.get("metadata", {})

                    # Formatar informações do passo
                    step_info = f"Step {i}:\n" f"{'='*50}\n" f"{content}\n" f"{'='*50}\n"
                    if metadata:
                        step_info += f"Metadata: {metadata}\n"

                    await console.print(step_info)
            else:
                await console.error("Development task failed")

        finally:
            await client.cleanup()

    except Exception as e:
        await console.error("Error during development", str(e))


async def demonstrate_code_review() -> None:
    """Demonstrate collaborative code review"""
    try:
        await console.info("🤖 Initializing Review Team...")

        # Criar configuração do AI usando valores padrão do ambiente
        ai_config = AIConfig()

        # Criar cliente AI
        client = AIClient(ai_config)
        await client.initialize()

        try:
            team = await setup_development_team(client)

            # Código para revisão
            code_to_review = """
            def cache_decorator(timeout=300, max_size=100):
                cache = {}
                
                def decorator(func):
                    def wrapper(*args, **kwargs):
                        key = str(args) + str(kwargs)
                        if key in cache:
                            return cache[key]
                        result = func(*args, **kwargs)
                        cache[key] = result
                        return result
                    return wrapper
                return decorator
            """

            # Configurar tarefa de revisão
            review_task = f"""
            Review the following code implementation:
            
            {code_to_review}
            
            Focus on:
            1. Thread safety
            2. Memory management
            3. Error handling
            4. Edge cases
            5. Performance implications
            """

            await console.info("📋 Starting Code Review", title="Review Task", content=review_task)

            # Executar revisão
            result = await team.execute_task(review_task)

            if result.success:
                await console.success(
                    "Review completed",
                    title="🔍 Review Results",
                    content=get_content(result.output),
                )
            else:
                await console.error("Code review failed")

        finally:
            await client.cleanup()

    except Exception as e:
        await console.error("Error during code review", str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_code_development())
    asyncio.run(demonstrate_code_review())
