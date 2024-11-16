"""AI agent examples demonstrating multi-agent system capabilities"""

import asyncio

from pepperpy.ai import AIClient
from pepperpy.ai.agents import ResearchAgent
from pepperpy.ai.templates import PromptTemplate, TemplateRegistry
from pepperpy.ai.types import AIResponse
from pepperpy.console import Console

console = Console()


def get_content(response: str | AIResponse) -> str:
    """Extract content from response"""
    if isinstance(response, AIResponse):
        return response.content
    return response


# Registrar templates personalizados
TemplateRegistry.register(
    "detailed_analysis",
    PromptTemplate(
        template=(
            "Topic: {topic}\n\n"
            "Please provide a detailed analysis considering:\n"
            "1. Historical context\n"
            "2. Current state\n"
            "3. Future implications\n"
            "4. Practical applications\n\n"
            "Additional considerations: {context}"
        ),
        validator={
            "topic": str,
            "context": str,
        },
        description="Template for detailed topic analysis",
    ),
)


async def demonstrate_research_agent() -> None:
    """Demonstrate research agent capabilities"""
    try:
        console.info("🤖 Initializing Research Agent...")

        client = await AIClient.create()
        async with client:
            agent = ResearchAgent(
                client=client,
                name="Research Expert",
                description="Advanced research and analysis specialist",
            )

            # Adicionar template personalizado
            agent.add_template(
                "custom_research",
                PromptTemplate(
                    "Analyze the following topic in depth:\n{topic}\n\n"
                    "Consider these specific aspects:\n{aspects}",
                ),
            )

            # Executar pesquisa
            topic = "The impact of artificial intelligence on software development"
            console.info(f"📚 Researching: {topic}")

            # Planejar a pesquisa
            steps = await agent.plan(f"Research and analyze the topic: {topic}")
            console.info("🗺️ Research Plan:")
            for i, step in enumerate(steps, 1):
                await console.print(f"  {i}. {step}")

            # Executar análise
            analysis = await agent.execute(
                topic,
                context="Focus on practical implications for developers",
            )
            console.success(
                "Analysis completed",
                title="🔍 Analysis Results",
                content=get_content(analysis)
            )

            # Avaliar fontes com critérios específicos
            evaluation = await agent.evaluate(
                content=get_content(analysis),
                criteria="Focus on methodology and data quality",
            )
            console.info(f"⚖️ Quality Evaluation: {get_content(evaluation)}")

            # Gerar resumo
            content_to_summarize = get_content(analysis)
            summary = await agent.summarize(content_to_summarize)
            console.success(
                "Summary generated",
                title="📝 Executive Summary",
                content=get_content(summary)
            )

    except Exception as e:
        console.error("Error during research", str(e))


if __name__ == "__main__":
    try:
        asyncio.run(demonstrate_research_agent())
    except KeyboardInterrupt:
        console.info("\n👋 Research finished!")
