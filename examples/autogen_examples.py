"""AutoGen examples demonstrating multi-agent collaboration"""

import asyncio
import os
from typing import Optional, Union

from pepperpy.ai import AIClient
from pepperpy.ai.autogen.agents import (
    CoderAgent,
    CriticAgent,
    ExecutorAgent,
    PlannerAgent,
)
from pepperpy.ai.autogen.agents.team import AgentTeam, TeamConfig
from pepperpy.ai.types import AIResponse
from pepperpy.console import Console
from pepperpy.core.config import AIConfig

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

    return AgentTeam(agents=[planner, coder, executor, critic], config=team_config)


async def demonstrate_code_development() -> None:
    """Demonstrate collaborative code development"""
    try:
        console.info("🤖 Initializing Development Team...")

        # Criar configuração do AI com valores padrão para campos opcionais
        ai_config = AIConfig(
            name="ai",
            version="1.0.0",
            provider="openrouter",
            api_key=os.getenv("OPENROUTER_API_KEY", ""),  # Valor padrão vazio
            model="anthropic/claude-3-sonnet",
            temperature=0.7,  # Valor padrão
            max_tokens=1000,  # Valor padrão
        )

        # Criar cliente AI diretamente com a configuração
        client = AIClient(config=ai_config)
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

            console.info(f"📋 Starting Development Task\n\n{task}", title="Task Definition")

            # Executar tarefa com o time
            result = await team.execute_task(task)

            if result.success:
                console.success(
                    "Development completed",
                    title="🎉 Final Result",
                    content=get_content(result.output),
                )

                # Mostrar passos do desenvolvimento
                console.info("📝 Development Steps:")
                for i, step in enumerate(result.steps, 1):
                    content = step["content"]
                    metadata = step.get("metadata", {})

                    # Formatar informações do passo
                    step_info = f"Step {i}:\n" f"{'='*50}\n" f"{content}\n" f"{'='*50}\n"
                    if metadata:
                        step_info += f"Metadata: {metadata}\n"

                    await console.print(step_info)
            else:
                console.error("Development task failed")

        finally:
            await client.cleanup()

    except Exception as e:
        console.error("Error during development:", str(e))


async def demonstrate_code_review() -> None:
    """Demonstrate collaborative code review"""
    try:
        console.info("🤖 Initializing Review Team...")

        # Criar configuração do AI com valores padrão para campos opcionais
        ai_config = AIConfig(
            name="ai",
            version="1.0.0",
            provider="openrouter",
            api_key=os.getenv("OPENROUTER_API_KEY", ""),  # Valor padrão vazio
            model="anthropic/claude-3-sonnet",
            temperature=0.7,  # Valor padrão
            max_tokens=1000,  # Valor padrão
        )

        # Criar cliente AI diretamente com a configuração
        client = AIClient(config=ai_config)
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

            console.info(f"📋 Starting Code Review\n\n{review_task}", title="Review Task")

            # Executar revisão
            result = await team.execute_task(review_task)

            if result.success:
                console.success(
                    "Review completed",
                    title="🔍 Review Results",
                    content=get_content(result.output),
                )
            else:
                console.error("Code review failed")

        finally:
            await client.cleanup()

    except Exception as e:
        console.error("Error during code review:", str(e))


if __name__ == "__main__":
    asyncio.run(demonstrate_code_development())
    asyncio.run(demonstrate_code_review())
